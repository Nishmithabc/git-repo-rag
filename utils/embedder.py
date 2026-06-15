from sentence_transformers import SentenceTransformer

# Loading the model once when the application starts
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Converts each chunk into an embedding vector.
    """

    # Extract only the text content from each chunk
    texts = [chunk["content"] for chunk in chunks]

    # Generate embeddings
    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings

def generate_query_embedding(question: str):
    """
    Generates embedding for a user question.
    Used during retrieval.
    """
    embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    return embedding