from copy import deepcopy

def chunk_documents(documents, chunk_size=800, chunk_overlap=100):

    chunks = []

    for document in documents:
        content = document["content"]
        metadata = document["metadata"]

        start = 0
        chunk_id = 0

        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]

            # Copy metadata and add chunk id
            chunk_metadata = deepcopy(metadata)
            chunk_metadata["chunk_id"] = chunk_id

            chunks.append({
                "content": chunk_text,
                "metadata": chunk_metadata
            })

            chunk_id += 1
            start += (chunk_size - chunk_overlap)

    return chunks
