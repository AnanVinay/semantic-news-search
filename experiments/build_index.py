import numpy as np
import pickle
import faiss

from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text
from src.embeddings.embedder import Embedder
from src.clustering.fuzzy_cluster import FuzzyClusterer

print("Loading dataset...")

dataset_path = "data/20_newsgroups/20_newsgroups"
df = load_20newsgroups(dataset_path)

print("Cleaning text...")
df["clean_text"] = df["text"].apply(clean_text)

documents = df["clean_text"].tolist()

print("Generating embeddings...")
embedder = Embedder()
embeddings = embedder.encode_documents(documents)

print("Saving embeddings...")
np.save("models/embeddings.npy", embeddings)

print("Saving documents...")
with open("models/documents.pkl", "wb") as f:
    pickle.dump(documents, f)

print("Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "models/faiss.index")

print("Running clustering...")
clusterer = FuzzyClusterer(n_clusters=12)
clusterer.fit(embeddings)

print("Saving clustering model...")
with open("models/cluster_model.pkl", "wb") as f:
    pickle.dump(clusterer, f)

print("Index build complete!")