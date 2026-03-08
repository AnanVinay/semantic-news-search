import re


def remove_headers(text):
    
    parts = text.split("\n\n", 1)

    if len(parts) > 1:
        return parts[1]

    return text


def remove_quotes(text):
   

    lines = text.split("\n")

    filtered_lines = []

    for line in lines:
        if not line.strip().startswith(">"):
            filtered_lines.append(line)

    return "\n".join(filtered_lines)


def clean_text(text):
    

    text = remove_headers(text)

    text = remove_quotes(text)

    text = text.lower()

    text = re.sub(r"\S+@\S+", "", text)

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()