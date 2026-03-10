from fastapi import FastAPI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ---------- Load once when server starts ----------
INDEX_NAME = os.getenv("PINECONE_INDEX")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

# ---------- API endpoint ----------
@app.post("/ask")
def ask(question: str):

    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        return {"answer": "No relevant information found"}

    context = " ".join([doc.page_content for doc in docs])

    return {"answer": context}