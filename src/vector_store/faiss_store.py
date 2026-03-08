import faiss
import numpy as np


class FaissVectorStore:

    def __init__(self, dimension):

        self.dimension = dimension

        # L2 distance index
        self.index = faiss.IndexFlatL2(dimension)

        # store original documents
        self.documents = []

    def add_documents(self, embeddings, documents):

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)

        self.documents.extend(documents)

    def search(self, query_embedding, top_k=5):

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            results.append(self.documents[idx])

        return results