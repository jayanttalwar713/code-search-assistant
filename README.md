# Context-Aware Code Search Assistant

## Overview
This project is a lightweight semantic search tool for navigating and exploring a codebase using natural language queries.

Instead of relying on keyword search, it uses embeddings to understand meaning and retrieve the most relevant files from a project.

The system is designed as a prototype exploring ideas in search, context management, and agent-like workflows.

---

## Features

- Semantic search over code using transformer embeddings
- Fast similarity search using FAISS
- Lightweight context memory (previous queries influence search)
- Two-mode system:
  - Search mode (find relevant files)
  - Overview mode (high-level file inspection)
- Progress bar during indexing for better UX
- Filters out irrelevant directories (venv, site-packages, etc.)

---

## How It Works

1. The codebase is scanned and relevant source files are loaded.
2. Each file is converted into a vector embedding using a sentence transformer model.
3. FAISS builds an index for fast similarity search.
4. User queries are embedded and compared against stored vectors.
5. The system returns the most relevant file paths and snippets.
6. For “overview-style” queries, the system switches to a summary view.

---

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt

### 2. Run the Program
```bash
python Pacific.py

### 3. Provide the codebase path
When prompted, enter the path to a folder containing source code.



Example Queries
Where is authentication handled?
Which files relate to the UI?
Where is the prediction model defined?
What parts of the code handle data processing?



