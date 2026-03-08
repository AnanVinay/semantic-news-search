import os
import pandas as pd


def load_20newsgroups(dataset_path):

    texts = []
    labels = []

    print("Scanning dataset folder...")

    for category in os.listdir(dataset_path):

        category_path = os.path.join(dataset_path, category)

        if not os.path.isdir(category_path):
            continue

        print("Loading category:", category)

        for filename in os.listdir(category_path):

            file_path = os.path.join(category_path, filename)

            try:
                with open(file_path, "r", encoding="latin1") as f:

                    content = f.read()

                    texts.append(content)
                    labels.append(category)

            except:
                continue

    df = pd.DataFrame({
        "text": texts,
        "category": labels
    })

    return df