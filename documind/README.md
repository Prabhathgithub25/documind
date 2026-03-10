# DocuMind

DocuMind is a document intelligence system that allows users to ask questions from uploaded documents and receive accurate answers.

The system converts documents into vector embeddings and stores them in Pinecone for efficient retrieval.

Technologies Used
- Python
- FastAPI
- LangChain
- HuggingFace Embeddings
- Pinecone Vector Database

Features
- Document ingestion and chunking
- Semantic search using vector embeddings
- FastAPI based REST API
- Rate limiting for API protection
- Logging and error handling
- Health check endpoint

API Endpoints
GET /           - API status
GET /health     - Service health check
POST /ask       - Ask questions from documents

How to Run

1. Activate virtual environment  
venv\Scripts\activate

2. Run ingestion  
python ingest.py

3. Start API server  
uvicorn app:app --reload

Then open:
http://127.0.0.1:8000/docs