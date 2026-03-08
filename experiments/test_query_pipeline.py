from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text
from src.embeddings.embedder import Embedder
from src.vector_store.faiss_store import FaissVectorStore
from src.clustering.fuzzy_cluster import FuzzyClusterer
from src.cache.semantic_cache import SemanticCache


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

    print("Running clustering...")
    clusterer = FuzzyClusterer(n_clusters=12)
    membership = clusterer.fit(embeddings)

    print("Initializing semantic cache...")
    cache = SemanticCache(threshold=0.85)

    print("\nSystem ready.\n")

    while True:

        query = input("Enter query (or 'exit'): ")

        if query.lower() == "exit":
            break

        # embed query
        query_embedding = embedder.encode_query(query)

        # detect dominant cluster
        cluster_id = clusterer.model.predict(
            clusterer.pca.transform(
                clusterer.scaler.transform(query_embedding)
            )
        )[0]

        print("Detected cluster:", cluster_id)

        # check cache
        hit, entry, score = cache.lookup(query_embedding)

        if hit:

            print("\nCACHE HIT")
            print("Matched query:", entry["query"])
            print("Similarity:", score)
            print("Result:\n", entry["result"][:500])

        else:

            print("\nCACHE MISS — performing vector search")

            results = vector_store.search(query_embedding, top_k=3)

            result_text = "\n---\n".join(results)

            # store in cache
            cache.store(query, query_embedding, result_text, cluster_id)

            print("\nSearch results:\n")
            print(result_text[:500])

        print("\nCache stats:", cache.stats())
        print()


if __name__ == "__main__":
    main()