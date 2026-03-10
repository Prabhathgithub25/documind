from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Create limiter
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."},
    )

@app.post("/ask")
def ask(question: str):

    logger.info(f"Received question: {question}")

    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        logger.warning("No documents found for the query")
        return {"answer": "No relevant information found"}

    context = " ".join([doc.page_content for doc in docs])

    logger.info("Answer retrieved successfully")

    return {"answer": context}