## this is a single turn chatbot here 
## Here we implement tracing of all parts of this application not only the runnables parts (i.e. where there is invoke method)
# as we set run name so default RunnableSequence will not be here as run_name
# no extra metadata apart from from defualt storage will be stored as we not storing anything explicitly
# here two different pipelines will be created, setup_pipeline (this will trace pdf load, chunking, embedding) and pdf_rag_query (will trace actual q&a part) - in rag_v3.py we will fix this by putting under one trace.
# attach metadata

# in v4, we will store the vector store and load in next run instead of recreating embeddings at each time a question is asked


# this is the part we have to add to trace all parts of the RAG
from langsmith import traceable

import json
import hashlib
from pathlib import Path


import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# expects OPENAI_API_KEY in .env
load_dotenv()


# set project name (here  set this name post load_dotenv() othersise this name will be overwritted by env file's project name)
os.environ["LANGCHAIN_PROJECT"] = "RAG Chatbot"


# this path should be changed according to path and name of pdf file
PDF_PATH = 'islr.pdf'


# variables to load to store the vector store to store embeddings
INDEX_ROOT = Path(".indices")
INDEX_ROOT.mkdir(exist_ok=True)


# ------------------------ helpers (traced individually) -------------------------------

# We have to add decoartor traceable for each part as shown below, before that all required parts should be wraped in functions, then apply decorator


# 1) Load PDF
@traceable(name = "load_pdf", tags = ["pdf", "loader"], metadata = {'loader': 'PyPDFLoader'})
def load_pdf(path: str):
    loader = PyPDFLoader(PDF_PATH)
    return loader.load() # it will create one document per page

# 2) Chunk
@traceable(name = "split_documenents")
def split_documents(docs, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )

    return splitter.split_documents(docs)

@traceable(name = "build_vectorstore")
def build_vectorstore(splits, embed_model_name: str):
    emb = OpenAIEmbeddings(model = embed_model_name)
    # FAISS.from_documents internally calls the embedding model:
    vs = FAISS.from_documents(splits, emb)
    return vs

# ------------------------ cache key / fingerprint --------------------
def _file_fingerprint(path: str) -> dict:
    p = Path(path)
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return {"sha256": h.hexdigest(), "size": p.stat().st_size, "mtime": int(p.stat().st_mtime)}

def _index_key(pdf_path: str, chunk_size: int, chunk_overlap: int, embed_model_name: str) -> str:
    meta = {
        "pdf_fingerprint": _file_fingerprint(pdf_path),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "embedding_model": embed_model_name,
        "format": "v1"
    }
    return hashlib.sha256(json.dumps(meta, sort_keys=True).encode("utf-8")).hexdigest()


# --------------------- explicitly traced load/build runs ------------------------

# 3) Embedding + Indexing
@traceable(name = "load_index", tags = ['index'])
def load_index_run(index_dir: Path, embed_model_name: str):
    emb = OpenAIEmbeddings(model = embed_model_name)
    # FAISS.from_documents internally calls the embedding model:
    return FAISS.from_local(
        str(index_dir),
        emb,
        allow_dangerous_deserialization = True
        )

@traceable(name="build_index", tags=["index"])
def buil_index_run(pdf_path: str, index_dir: Path, chunk_size: int, chunk_overlap: int, embed_model_name: str):
    docs = load_pdf(pdf_path)
    splits = split_documents(docs, chunk_size= chunk_size, chunk_overlap=chunk_overlap)
    vs = build_vectorstore(splits, embed_model_name)
    index_dir.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(index_dir))
    (index_dir/"meta.json").write_text(json.dumps({
        "pdf_path": os.path.abspath(pdf_path),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "embedding_model": embed_model_name
    }, indent=2))
    return vs

# ---------------------- dispatcher (not traced) --------------------
def load_or_build_index(
        pdf_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        embed_model_name: str = 'text-embedding-3-small',
        force_rebuild: bool = False
):
    key = _index_key(pdf_path, chunk_size, chunk_overlap, embed_model_name)
    index_dir = INDEX_ROOT / key
    cache_hit = index_dir.exists() and not force_rebuild
    if cache_hit:
        return load_index_run(index_dir, embed_model_name)
    else:
        return buil_index_run(pdf_path, index_dir, chunk_size, chunk_overlap, embed_model_name)


# ------------- parent setup function (traced) ------------------------
@traceable(name = "setup_pipeline", tags=["setup"])
def setup_pipeline(pdf_path: str, chunk_size = 1000, chunk_overlap = 150, embed_model_name = "text-embedding-3-small", force_rebuild = False):
    return load_or_build_index(
        pdf_path=pdf_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embed_model_name=embed_model_name,
        force_rebuild=force_rebuild,
    )

# --------------------------- model, prompt and run ---------------------

llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

# ----------------------- one top-level (root) run --------------------------------
@traceable(name="pdf_rag_full_run")
def setup_pipeline_and_query(pdf_path: str, question: str):
    # Parent setup run (child of root)]
    vectorstore = setup_pipeline(pdf_path, chunk_size = 1000, chunk_overlap = 150)
    retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs = {"k": 4})

    parallel = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    chain = parallel | prompt | llm | StrOutputParser()

    # this LangChain run stays under the same root (since we're inside this traced function)
    lc_config = {"run_name": "pdf_rag_query"}
    return chain.invoke(question, config = lc_config)

# --------------- CLI ----------------------
if __name__ == "__main__":
    print("PDF RAG ready. ask a question (or Ctrl+C to exit).")
    q = input("\nQ: ")
    ans = setup_pipeline_and_query(PDF_PATH, q)
    print("\nA:", ans)
