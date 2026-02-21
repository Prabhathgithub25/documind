import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FakeEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# --- make FakeEmbeddings return Python float (not float64) ---
class FloatEmbeddings(FakeEmbeddings):
    def embed_documents(self, texts):
        vecs = super().embed_documents(texts)
        return [list(map(float, v)) for v in vecs]

    def embed_query(self, text):
        v = super().embed_query(text)
        return list(map(float, v))

load_dotenv()

# -------- Load PDFs --------
loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
print(f"Loaded {len(documents)} pages")

# -------- Chunking --------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# -------- Embeddings (FREE, 384-dim) --------
embeddings = FloatEmbeddings(size=384)

# -------- Pinecone Setup --------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

existing = [i.name for i in pc.list_indexes().indexes]
if index_name not in existing:
    pc.create_index(
        name=index_name,
        dimension=384,        # MUST match embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print("Pinecone Index Created")

# -------- Store Vectors --------
vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=index_name
)

print("Ingestion Completed Successfully")