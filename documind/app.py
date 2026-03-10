from fastapi import FastAPI, HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

INDEX_NAME = os.getenv("PINECONE_INDEX")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

@app.post("/ask")
def ask(question: str):

    # 1️⃣ Check empty query
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 2️⃣ Retrieve documents
    docs = vectorstore.similarity_search(question, k=3)

    # 3️⃣ If no relevant documents
    if not docs:
        return {"answer": "No relevant information found in the documents."}

    context = " ".join([doc.page_content for doc in docs])

    return {"answer": context}