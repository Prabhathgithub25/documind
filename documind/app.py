from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import logging

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

# rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# -------------------------
# Example vectorstore (replace with your real one)
# -------------------------
vectorstore = None


# home route
@app.get("/")
def home():
    return {"message": "DocuMind API running successfully"}


# rate limit error handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."},
    )


# ask endpoint with rate limit
@app.post("/ask")
@limiter.limit("10/minute")
def ask(request: Request, question: str):

    try:

        logger.info(f"Received question: {question}")

        docs = vectorstore.similarity_search(question, k=3)

        if not docs:
            logger.warning("No documents found")
            return {"answer": "No relevant information found"}

        context = " ".join([doc.page_content for doc in docs])

        logger.info("Answer generated successfully")

        return {"answer": context}

    except Exception as e:

        logger.error(f"System error: {str(e)}")

        return {
            "error": "Internal server error",
            "message": str(e)
        }