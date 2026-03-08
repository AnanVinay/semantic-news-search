from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text
from src.embeddings.embedder import Embedder


def main():

    dataset_path = "data/20_newsgroups/20_newsgroups"

    print("Loading dataset...")
    df = load_20newsgroups(dataset_path)

    print("Total documents:", len(df))

    print("\nCleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    print("Sample cleaned text:\n")
    print(df["clean_text"].head())

    print("\nInitializing embedding model...")
    embedder = Embedder()

    print("\nGenerating embeddings for all documents...")

    embeddings = embedder.encode_documents(df["clean_text"].tolist())

    print("\nEmbeddings generated successfully!")

    print("Embedding matrix shape:", embeddings.shape)

    print("\nExample embedding vector (first document):\n")
    print(embeddings[0][:10])  # print first 10 numbers


if __name__ == "__main__":
    main()