## this is a single turn chatbot here 
## Here we implement tracing of all parts of this application not only the runnables parts (i.e. where there is invoke method)
# as we set run name so default RunnableSequence will not be here as run_name
# no extra metadata apart from from defualt storage will be stored as we not storing anything explicitly
# here two different pipelines will be created, setup_pipeline (this will trace pdf load, chunking, embedding) and pdf_rag_query (will trace actual q&a part) - in rag_v3.py we will fix this by putting under one trace.

# this is the part we have to add to trace all parts of the RAG
from langsmith import traceable


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





# ------------------------ traced setup steps -------------------------------

# We have to add decoartor traceable for each part as shown below, before that all required parts should be wraped in functions, then apply decorator


# 1) Load PDF
@traceable(name = "load_pdf")
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

# 3) Embedding + Indexing
@traceable(name = "build_vectorstore")
def build_vectorstore(splits):
    emb = OpenAIEmbeddings(model = 'text-embedding-3-small')
    # FAISS.from_documents internally calls the embedding model:
    vs = FAISS.from_documents(splits, emb)
    return vs

# You can also traceba "setup" umbrella span if you want
@traceable(name = "setup_pipeline")
def setup_pipeline(pdf_path: str):
    docs = load_pdf(pdf_path)
    splits = split_documents(docs)
    vs = build_vectorstore(splits)
    return vs

# --------------------------- pipeline ---------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

# 5) Chain
llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

vectorstore = setup_pipeline(PDF_PATH)
retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs = {"k": 4})

parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()

# 6) Ask questions
print("PDF RAG ready. ask a question (or Ctrl+C to exit).")
q = input("\nQ: ")

config = {
        "run_name": 'pdf_rag_query'
}
ans = chain.invoke(q.strip())
print("\nA:", ans)
