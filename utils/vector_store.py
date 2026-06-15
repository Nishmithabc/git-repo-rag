from pathlib import Path
import pickle
import faiss
import numpy as np

VECTOR_STORE_DIR = Path("vector_store")
VECTOR_STORE_DIR.mkdir(exist_ok=True)


def save_to_vector_store(repo_name, chunks, embeddings):
    """
    Saves normalized embeddings to a FAISS IndexFlatIP
    and stores chunk content + metadata separately.
    """

    # Convert to float32 (required by FAISS)
    embeddings = np.array(embeddings).astype("float32")

    # Normalize embeddings (L2 normalization)
    faiss.normalize_L2(embeddings)

    # Create Inner Product index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(
        index,
        str(VECTOR_STORE_DIR / f"{repo_name}.index")
    )

    # Save chunks (content + metadata)
    with open(
        VECTOR_STORE_DIR / f"{repo_name}_chunks.pkl",
        "wb"
    ) as f:
        pickle.dump(chunks, f)

    print(f"Saved {index.ntotal} vectors to FAISS.")