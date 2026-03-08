import numpy as np
import pickle
import faiss

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.vector_store.faiss_store import FaissVectorStore
from src.embeddings.embedder import Embedder
from src.cache.semantic_cache import SemanticCache

print("Loading precomputed models...")

with open("models/documents.pkl", "rb") as f:
    documents = pickle.load(f)

embeddings = np.load("models/embeddings.npy")

index = faiss.read_index("models/faiss.index")

with open("models/cluster_model.pkl", "rb") as f:
    clusterer = pickle.load(f)

vector_store = FaissVectorStore(dimension=384)
vector_store.index = index
vector_store.documents = documents

embedder = Embedder()

cache = SemanticCache(threshold=0.75)

print("System ready!")

app = FastAPI(title="Semantic News Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()


class QueryRequest(BaseModel):
    query: str



@app.post("/query")
def query_endpoint(request: QueryRequest):

    query = request.query

    query_embedding = embedder.encode_query(query)

    cluster_id = clusterer.model.predict(
        clusterer.pca.transform(
            clusterer.scaler.transform(query_embedding)
        )
    )[0]

    hit, entry, score = cache.lookup(query_embedding)

    if hit:
        return {
            "query": query,
            "cache_hit": True,
            "matched_query": entry["query"],
            "similarity_score": float(score),
            "result": entry["result"],
            "dominant_cluster": int(cluster_id)
        }

    results = vector_store.search(query_embedding, top_k=3)

    result_text = "\n---\n".join(results)

    cache.store(query, query_embedding, result_text, cluster_id)

    return {
        "query": query,
        "cache_hit": False,
        "matched_query": None,
        "similarity_score": None,
        "result": result_text,
        "dominant_cluster": int(cluster_id)
    }



@app.get("/cache/stats")
def cache_stats():
    return cache.stats()



@app.delete("/cache")
def clear_cache():
    cache.clear()
    return {"message": "Cache cleared"}