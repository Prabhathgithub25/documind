import warnings
warnings.filterwarnings("ignore")

import os
import re
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX")

# ---------- Embeddings ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------- Load Vector Store ----------
vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

print("DocuMind Week-2 Ready (type 'exit' to stop)")

# ---------- Simple Answer Extractor ----------
def extract_answer(context, question):
    text = context.lower()
    q = question.lower()

    # joining date
    if "joining" in q or "date" in q:
        match = re.search(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', context)
        if match:
            return match.group(0)

    # salary / stipend
    if "salary" in q or "stipend" in q:
        match = re.search(r'₹?\s?\d{1,3}(?:,\d{3})*(?:\s?per\s?month)?', context, re.IGNORECASE)
        if match:
            return match.group(0)

    # company / issued by
    if "who issued" in q or "company" in q:
        lines = context.split("\n")
        for line in lines:
            if "solutions" in line.lower() or "company" in line.lower():
                return line.strip()

    return context[:300]  # fallback (first part only)


while True:
    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    docs = vectorstore.similarity_search(question, k=5)

    if not docs:
        print("\nAnswer: Not found")
        continue

    context = " ".join([doc.page_content for doc in docs])

    answer = extract_answer(context, question)

    print("\nAnswer:", answer)