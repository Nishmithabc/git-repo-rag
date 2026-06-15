import os
import shutil
import zipfile
from pathlib import Path

from fastapi import UploadFile

from utils.document_loader import load_repository
from utils.chunker import chunk_documents
from utils.embedder import generate_embeddings
from utils.vector_store import save_to_vector_store

TEMP_DIR = Path("temp")
UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".md",
    ".txt"
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "dist",
    "build",
    ".idea",
    ".vscode"
}


async def repo_process(zip_file: UploadFile):
    
    # Create necessary directories
    TEMP_DIR.mkdir(exist_ok=True)
    UPLOAD_DIR.mkdir(exist_ok=True)

    # Save uploaded ZIP
    zip_path = TEMP_DIR / zip_file.filename

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    # Validate ZIP
    if not zipfile.is_zipfile(zip_path):
        zip_path.unlink()
        raise ValueError("Uploaded file is not a valid ZIP archive.")

    # Extract ZIP
    repo_name = zip_path.stem
    extract_path = TEMP_DIR / repo_name

    if extract_path.exists():
        shutil.rmtree(extract_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Destination folder for filtered files
    destination = UPLOAD_DIR / repo_name

    if destination.exists():
        shutil.rmtree(destination)

    destination.mkdir(parents=True)

    indexed_files = []

    # Traverse extracted repository
    for root, dirs, files in os.walk(extract_path):

        # Skip unwanted folders
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:
            file_path = Path(root) / file

            if file_path.suffix.lower() in ALLOWED_EXTENSIONS:

                relative_path = file_path.relative_to(extract_path)

                target_path = destination / relative_path
                target_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.copy2(file_path, target_path)

                indexed_files.append(str(relative_path))

    # Load repository files into documents
    documents = load_repository(destination)

    chunks = chunk_documents(documents)

    # Generate embeddings for the chunks
    embeddings = generate_embeddings(chunks)

    # Save embeddings and chunk metadata to vector store
    save_to_vector_store(repo_name, chunks, embeddings)

    # Keep temp files for now (helpful for debugging)
    os.remove(zip_path)
    shutil.rmtree(extract_path)

    return {
        "repo_name": repo_name,
        "files": indexed_files,
        "documents": documents,
        "chunks": chunks,
        "embeddings": embeddings.tolist()
    }