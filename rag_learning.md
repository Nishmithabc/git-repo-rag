# GitHub Repository RAG Assistant

## Overview

GitHub Repository RAG Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload a GitHub repository as a ZIP file and interact with it through natural language questions.

Instead of manually browsing source files, users can ask questions such as:

* *"How is the YouTube URL validated?"*
* *"What is the workflow for generating summaries?"*
* *"How are transcripts retrieved?"*

The system semantically searches the repository codebase, retrieves the most relevant code snippets, and uses a Large Language Model (LLM) to generate context-aware answers grounded only in the uploaded repository.

---

## Problem Statement

Understanding unfamiliar codebases can be time-consuming, especially for large projects. Developers often spend significant effort locating relevant files, reading implementation details, and tracing application workflows.

Traditional keyword search is limited because it relies on exact matches and does not understand the semantic meaning of a question.

This project addresses that challenge by applying Retrieval-Augmented Generation (RAG) to source code repositories, enabling semantic code search and repository-aware question answering.

---

## Solution

The application processes an uploaded GitHub repository in the following stages:

1. **Repository Upload**

   * Accepts a repository ZIP file through a FastAPI endpoint.
   * Validates and extracts the archive.

2. **Repository Parsing**

   * Recursively traverses the extracted project.
   * Ignores unnecessary folders (`.git`, `venv`, `node_modules`, etc.).
   * Retains only relevant source code and documentation files.

3. **Document Loading**

   * Reads each file's content.
   * Attaches metadata such as file name, relative path, extension, and chunk identifier.

4. **Chunking**

   * Splits large files into overlapping text chunks.
   * Preserves contextual continuity for better retrieval.

5. **Embedding Generation**

   * Converts chunks into dense vector embeddings using a Sentence Transformer model.

6. **Vector Database Storage**

   * Normalizes embeddings and stores them in a FAISS vector index using cosine similarity (Inner Product with L2 normalization).
   * Stores corresponding chunk metadata separately for retrieval.

7. **Question Answering**

   * Converts the user question into an embedding.
   * Retrieves the top-k semantically similar chunks using FAISS.
   * Filters low-confidence results using a similarity threshold.
   * Builds a context prompt from the retrieved chunks.
   * Sends the context and question to an LLM (Groq-hosted Llama model).
   * Returns a grounded answer along with the source files used.

---

## System Architecture

```text
User Uploads Repository (.zip)
            │
            ▼
    Extract & Filter Files
            │
            ▼
      Load Documents
            │
            ▼
    Chunk Documents (800 chars, overlap)
            │
            ▼
 Generate Vector Embeddings
            │
            ▼
 Store Embeddings + Metadata
    (FAISS + Pickle Storage)
────────────────────────────────────
         User Question
            │
            ▼
   Generate Query Embedding
            │
            ▼
    FAISS Semantic Retrieval
            │
            ▼
 Retrieve Top-k Relevant Chunks
            │
            ▼
      Build Context Prompt
            │
            ▼
      Groq (Llama 3.x LLM)
            │
            ▼
    Repository-Grounded Answer
            │
            ▼
 Return Answer + Source Metadata
```

---

## Tech Stack

| Component        | Technology            |
| ---------------- | --------------------- |
| Backend API      | FastAPI               |
| Language         | Python                |
| Embedding Model  | Sentence Transformers |
| Vector Database  | FAISS                 |
| LLM              | Groq (Llama 3.x)      |
| Metadata Storage | Pickle                |
| Version Control  | Git & GitHub          |

---

## Features

* Upload GitHub repositories as ZIP archives.
* Recursive repository parsing and file filtering.
* Automatic source code chunking with overlap.
* Semantic code search using vector embeddings.
* Retrieval-Augmented Generation (RAG) pipeline.
* Repository-grounded answers with source attribution.
* Similarity threshold filtering to reduce hallucinations.
* Modular FastAPI backend for easy extension.

---

## Project Structure

```text
git_repo_rag/
│
├── main.py
├── routes/
│   ├── repo_extract.py
│   └── repo_chat.py
│
├── utils/
│   ├── repo_parsing.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── context_builder.py
│   └── llm.py
│
├── uploads/
├── temp/
├── vector_store/
├── .env
├── .gitignore
└── README.md
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd git_repo_rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Example Workflow

1. Upload a GitHub repository ZIP file.
2. The system extracts and indexes the repository.
3. Ask a question, for example:

```
How is the YouTube URL validated?
```

4. The application retrieves relevant code snippets and generates an answer using the LLM.
5. The response includes both the answer and the source files used for generation.

---

## Future Enhancements

* Direct GitHub repository URL ingestion.
* Multi-repository indexing and querying.
* Repository visualization and dependency graphs.
* Conversation memory for follow-up questions.
* Persistent vector database using ChromaDB or PostgreSQL with pgvector.
* Frontend interface for repository upload and chat.

---

## Learning Outcomes

This project was built to explore and understand the complete Retrieval-Augmented Generation (RAG) pipeline, including:

* Document ingestion and preprocessing.
* Text chunking strategies.
* Embedding generation.
* Vector databases and similarity search.
* Retrieval evaluation using similarity thresholds.
* Prompt engineering for grounded LLM responses.
* Integration of FastAPI, FAISS, Sentence Transformers, and Groq-hosted LLMs.
