## this is a single turn chatbot here 
## prob : LangSmith wil trace only runnable parts not other parts, it's designed like it
## prob: embedding vector is not getting stored, each time embeddings will be created freshy

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
# as we didn't set any run name so default RunnableSequence will be run_name, also no extra metadata apart from from defualt storage will be stored as we not storing anything explicitly


# this path should be changed according to path and name of pdf file
PDF_PATH = 'islr.pdf'

# 1) Load PDF
loader = PyPDFLoader(PDF_PATH)
docs = loader.load() # it will create one document per page

# 2) Chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 150
)

splits = splitter.split_documents(docs)

# 3) Embedding + Indexing
emb = OpenAIEmbeddings(model = 'text-embedding-3-small')
vs = FAISS.from_documents(splits, emb)
retriever = vs.as_retriever(search_type = "similarity", search_kwargs = {"k": 4})

# 4) Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

# 5) Chain
llm = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()

# 6) Ask questions
print("PDF RAG ready. ask a question (or Ctrl+C to exit).")
q = input("\nQ: ")
ans = chain.invoke(q.strip())
print("\nA:", ans)
