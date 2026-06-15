# GitHub Repository RAG - Learning Notes

## Objective

Build a Retrieval-Augmented Generation (RAG) chatbot that can understand a GitHub repository and answer questions about its codebase. The user uploads a repository as a ZIP file, and the system indexes the code for semantic retrieval.

# Overall Pipeline

User uploads GitHub ZIP
          ↓
Save ZIP temporarily
          ↓
Validate ZIP file
          ↓
Extract repository
          ↓
Filter useful source files
          ↓
Store filtered files in uploads/
          ↓
Load files into document objects
          ↓
Chunk the documents
          ↓
Generate embeddings
          ↓
Store embeddings in FAISS
          ↓
User asks question
          ↓
Embed question
          ↓
Retrieve relevant chunks
          ↓
Pass chunks + question to LLM
          ↓
Generate answer

# File-by-File Logic

## 1. `repo_parsing.py`

### Purpose
This file handles the ingestion of the uploaded GitHub repository.

### Workflow
1. Receive ZIP file from FastAPI endpoint.
2. Save the uploaded file into the `temp/` directory.
3. Verify that the uploaded file is a valid ZIP archive.
4. Extract the ZIP contents.
5. Recursively traverse the extracted repository.
6. Ignore unnecessary folders:
   - `.git`
   - `node_modules`
   - `venv`
   - `__pycache__`
   - `dist`
   - etc.
7. Copy only useful files to the `uploads/` directory.
   - `.py`
   - `.js`
   - `.ts`
   - `.java`
   - `.md`
   - `.txt`
   - etc.
8. Return the repository name and list of indexed files.

### Why use `temp/`?
`temp/` acts as a temporary workspace for ZIP extraction. It can later be cleaned up after processing to save storage.

### Why use `uploads/`?
`uploads/` stores only the filtered files that are actually useful for the RAG pipeline. These become the source of truth for later indexing.

## 2. `document_loader.py`

### Purpose
Convert the repository files into structured document objects.

### Input
A repository folder inside `uploads/`.

### Process
- Recursively visit every file.
- Open each file.
- Read its entire content.
- Create a document dictionary containing:
  - file content
  - metadata

Example:

```python
{
    "content": "...file text...",
    "metadata": {
        "file_name": "main.py",
        "relative_path": "main.py",
        "extension": ".py"
    }
}
```

### Why create document objects?
This provides a standard representation of data before chunking and embedding. Later pipeline stages work with documents instead of raw files.

---

## 3. `chunker.py`

### Purpose
Split large documents into smaller pieces that can be embedded and retrieved efficiently.

### Why chunk documents?

Large files often contain multiple unrelated concepts. Creating one embedding for an entire file would reduce retrieval accuracy.

Example:
- `main.py` may contain:
  - authentication
  - database logic
  - API routes
  - utility functions

Splitting it into chunks allows retrieval to focus on only the relevant section.

### Chunk Size

`chunk_size` defines the maximum amount of text placed into a single chunk.

Example:
- chunk_size = 300
- A file with 900 characters becomes approximately 3 chunks.

### Chunk Overlap

`chunk_overlap` determines how much text is shared between consecutive chunks.

Example:
- chunk_size = 300
- chunk_overlap = 50

```
Chunk 0 : characters 0   → 299
Chunk 1 : characters 250 → 549
Chunk 2 : characters 500 → 799
```

The overlapping 50 characters help preserve context across chunk boundaries.

### Why overlap is important

Without overlap, important code or sentences may be split exactly between two chunks, making retrieval less accurate.

Overlap ensures that neighboring chunks share context.

### Chunk Metadata

Each chunk inherits the metadata of its parent document and adds a `chunk_id`.

Example:

```python
{
    "content": "...chunk text...",
    "metadata": {
        "file_name": "main.py",
        "relative_path": "main.py",
        "extension": ".py",
        "chunk_id": 2
    }
}
```

This allows the system to identify exactly where retrieved information came from.

---

# Current Progress

## Completed
- [x] FastAPI project setup
- [x] ZIP upload endpoint
- [x] ZIP validation
- [x] Repository extraction
- [x] Recursive file traversal
- [x] Ignore unnecessary folders
- [x] Filter relevant code and documentation files
- [x] Store filtered files in `uploads/`
- [x] Load repository files as document objects
- [x] Chunk documents with overlap
- [x] Preserve metadata for every chunk

## Next Steps
- [ ] Understand embeddings
- [ ] Generate embeddings using Sentence Transformers
- [ ] Store vectors and metadata in FAISS
- [ ] Build retrieval pipeline
- [ ] Connect retrieval results to an LLM
- [ ] Create chat endpoint

---

# Key Concepts Learned

## What is a Document?
A structured representation of one source file containing:
- file content
- metadata

## What is a Chunk?
A smaller piece of a document created to improve retrieval accuracy.

## What is Chunk Size?
The maximum amount of text stored in one chunk.

## What is Chunk Overlap?
A small amount of shared text between adjacent chunks that preserves context.

## Why preserve metadata?
Metadata allows retrieved chunks to be traced back to their original source file.

---

# Important Insight

The RAG pipeline does not work directly on the original repository files.

```
Repository
    ↓
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
LLM Answer Generation
```

Each stage transforms the data into a format that is more suitable for the next stage.