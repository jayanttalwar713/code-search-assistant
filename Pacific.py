import os
import time
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

docs = []
paths = []
history = []

IGNORE_DIRS = {
    "venv",
    "site-packages",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode"
}

EXTENSIONS = (".py", ".js", ".ts", ".java")


def should_skip_path(path):
    return any(skip in path for skip in IGNORE_DIRS)


def load_codebase(folder):
    print("\n Scanning codebase...\n")

    for root, dirs, files in os.walk(folder):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        if should_skip_path(root):
            continue

        for file in files:
            if file.endswith(EXTENSIONS):
                path = os.path.join(root, file)

                if should_skip_path(path):
                    continue

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().strip()

                        if not text:
                            continue

                        docs.append(text)
                        paths.append(path)

                except:
                    continue

    print(f"\n Loaded {len(docs)} project files\n")


def build_index():
    print("Building embeddings...\n")

    embeddings = []

    for doc in tqdm(docs, desc="Embedding files"):
        emb = model.encode(doc)
        embeddings.append(emb)

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    print("\n Indexing vectors...")
    index.add(embeddings)

    print("Index ready!\n")
    return index


def is_overview_query(query):
    q = query.lower()
    triggers = [
        "what are the files about",
        "overview",
        "summarize",
        "what does this project do",
        "describe this codebase"
    ]
    return any(t in q for t in triggers)


def refine_query(query):
    if history:
        return query + " context: " + history[-1]
    return query


def search(query, index, k=5):
    q_emb = model.encode([query]).astype("float32")
    _, indices = index.search(q_emb, k)

    seen = set()
    results = []

    for i in indices[0]:
        if i not in seen:
            results.append(i)
            seen.add(i)

    return results

def overview_mode():
    print("\n PROJECT OVERVIEW MODE\n")

    show_n = min(8, len(paths))

    for i in range(show_n):
        snippet = docs[i][:400].replace("\n", " ")
        print(f"\n {paths[i]}")
        print(f"→ {snippet}...\n")


def main():
    folder = input("Enter codebase path: ")

    load_codebase(folder)
    index = build_index()

    print("\n Ready! Ask questions about the codebase.\n")

    while True:
        query = input(" Ask: ")

        print("\n Thinking...")

        history.append(query)
        refined = refine_query(query)

        if is_overview_query(query):
            overview_mode()
            continue

        results = search(refined, index)

        print("\n⚡ Quick Results (TTFT):")
        for i in results:
            print(f" {paths[i]}")


        print("\n Loading details...\n")
        time.sleep(0.7)

        for i in results:
            snippet = docs[i][:500].replace("\n", " ")
            print(f"\n {paths[i]}")
            print(f"→ {snippet}...\n")


if __name__ == "__main__":
    main()