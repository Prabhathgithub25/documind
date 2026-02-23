from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "DocuMind API Running"}

@app.post("/ask")
def ask_question(q: Question):
    return {
        "question_received": q.query,
        "answer": "This is a test response from DocuMind API"
    }