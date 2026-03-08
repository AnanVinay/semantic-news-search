from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:

    def __init__(self):
        

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode_documents(self, texts):

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=64
        )

        return np.array(embeddings)

    def encode_query(self, query):

        embedding = self.model.encode([query])

        return embedding