from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text
from src.embeddings.embedder import Embedder
from src.clustering.fuzzy_cluster import FuzzyClusterer


def main():

    dataset_path = "data/20_newsgroups/20_newsgroups"

    print("Loading dataset...")
    df = load_20newsgroups(dataset_path)

    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    print("Generating embeddings...")
    embedder = Embedder()

    embeddings = embedder.encode_documents(df["clean_text"].tolist())

    print("Running fuzzy clustering...")

    clusterer = FuzzyClusterer(n_clusters=12)

    membership = clusterer.fit(embeddings)

    print("Clustering complete")

    print("Membership matrix shape:", membership.shape)

    print("\nExample cluster memberships for first document:\n")

    print(membership[:, 0])


if __name__ == "__main__":
    main()