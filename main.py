import numpy as np
import pickle
import faiss

from fastapi import FastAPI
from pydantic import BaseModel

from src.vector_store.faiss_store import FaissVectorStore
from src.embeddings.embedder import Embedder
from src.cache.semantic_cache import SemanticCache

print("Loading precomputed models...")

# -------------------------
# Load stored artifacts
# -------------------------

with open("models/documents.pkl", "rb") as f:
    documents = pickle.load(f)

embeddings = np.load("models/embeddings.npy")

index = faiss.read_index("models/faiss.index")

with open("models/cluster_model.pkl", "rb") as f:
    clusterer = pickle.load(f)

# -------------------------
# Initialize components
# -------------------------

vector_store = FaissVectorStore(dimension=384)
vector_store.index = index
vector_store.documents = documents

embedder = Embedder()

cache = SemanticCache(threshold=0.75)

print("System ready!")


# -------------------------
# FastAPI app
# -------------------------

app = FastAPI(title="Semantic Search API")


class QueryRequest(BaseModel):
    query: str


# -------------------------
# Query endpoint
# -------------------------

@app.post("/query")
def query_endpoint(request: QueryRequest):

    query = request.query

    query_embedding = embedder.encode_query(query)

    # detect cluster
    cluster_id = clusterer.model.predict(
        clusterer.pca.transform(
            clusterer.scaler.transform(query_embedding)
        )
    )[0]

    # check cache
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

    # cache miss → search
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


# -------------------------
# Cache stats
# -------------------------

@app.get("/cache/stats")
def cache_stats():
    return cache.stats()


# -------------------------
# Clear cache
# -------------------------

@app.delete("/cache")
def clear_cache():
    cache.clear()
    return {"message": "Cache cleared"}