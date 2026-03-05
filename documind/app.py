from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
import time
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

app = FastAPI()

class Question(BaseModel):
    query: str

# Load embeddings once when server starts
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

INDEX_NAME = os.getenv("PINECONE_INDEX")

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

@app.get("/")
def home():
    return {"message": "DocuMind API Running"}

def stream_answer(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.03)

@app.post("/ask")
def ask_question(q: Question):

    docs = vectorstore.similarity_search(q.query, k=3)

    if not docs:
        return {"answer": "No relevant information found"}

    context = " ".join([doc.page_content for doc in docs])

    return StreamingResponse(
        stream_answer(context),
        media_type="text/plain"
    )