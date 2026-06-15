from pathlib import Path
import faiss
from utils.embedder import generate_query_embedding
import pickle
VECTOR_STORE_DIR = Path("vector_store")

def retrieve_chunks(repo_name, query, k=3):
    # Load FAISS index
    index_path = VECTOR_STORE_DIR / f"{repo_name}.index"
    if not index_path.exists():
        raise ValueError(f"No vector store found for repository: {repo_name}")

    index = faiss.read_index(str(index_path))

    # Load chunks
    chunks_path = VECTOR_STORE_DIR / f"{repo_name}_chunks.pkl"
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    # Generate embedding for the query
    query_embedding = generate_query_embedding(query)

    # Normalize query embedding
    faiss.normalize_L2(query_embedding)

    # Search for similar chunks
    distances, indices = index.search(query_embedding, k)

    retrieved_chunks = []
    retrieved_scores = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx < len(chunks):
            retrieved_chunks.append(chunks[idx])
            retrieved_scores.append(dist)

    return retrieved_chunks, retrieved_scores