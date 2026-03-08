import faiss
import numpy as np


class FaissVectorStore:

    def __init__(self, dimension):
        """
        Initialize FAISS index.

        dimension = embedding vector size (384 for MiniLM)
        """

        self.dimension = dimension

        # L2 distance index
        self.index = faiss.IndexFlatL2(dimension)

        # store original documents
        self.documents = []

    def add_documents(self, embeddings, documents):
        """
        Add document embeddings to the FAISS index
        """

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)

        self.documents.extend(documents)

    def search(self, query_embedding, top_k=5):
        """
        Search for most similar documents
        """

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            results.append(self.documents[idx])

        return results