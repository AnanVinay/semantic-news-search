from src.data_loader.load_dataset import load_20newsgroups
from src.preprocessing.clean_text import clean_text


dataset_path = "data/20_newsgroups/20_newsgroups"

print("Loading dataset...")

df = load_20newsgroups(dataset_path)

print("Cleaning documents...")

df["clean_text"] = df["text"].apply(clean_text)

print("\nCleaning complete")

print("Total documents:", len(df))

print("\nSample cleaned text:\n")

print(df["clean_text"].head())