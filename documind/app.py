from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

class Question(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "DocuMind API Running"}

# Fake streaming generator (simulates LLM token output)
def stream_answer(text: str):
    words = text.split()
    for word in words:
        yield word + " "
        time.sleep(0.05)   # simulate token delay

@app.post("/ask")
def ask_question(q: Question):
    answer_text = f"Streaming response for your question: {q.query}"
    return StreamingResponse(
        stream_answer(answer_text),
        media_type="text/plain"
    )