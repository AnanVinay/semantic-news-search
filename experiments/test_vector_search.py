from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text
from src.embeddings.embedder import Embedder
from src.vector_store.faiss_store import FaissVectorStore


def main():

    dataset_path = "data/20_newsgroups/20_newsgroups"

    print("Loading dataset...")
    df = load_20newsgroups(dataset_path)

    print("Cleaning documents...")
    df["clean_text"] = df["text"].apply(clean_text)

    print("Generating embeddings...")
    embedder = Embedder()

    embeddings = embedder.encode_documents(df["clean_text"].tolist())

    print("Building vector database...")

    vector_store = FaissVectorStore(dimension=384)

    vector_store.add_documents(embeddings, df["clean_text"].tolist())

    print("Vector database ready.")

    query = "space shuttle launch nasa mission"

    print("\nQuery:", query)

    query_embedding = embedder.encode_query(query)

    results = vector_store.search(query_embedding, top_k=5)

    print("\nTop similar documents:\n")

    for i, r in enumerate(results):
        print(f"Result {i+1}:\n", r[:300], "\n")


if __name__ == "__main__":
    main()