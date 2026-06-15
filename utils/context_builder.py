def build_context(retrieved_chunks):
    context = ""
    for chunk in retrieved_chunks:
        context += (
            f"File:{chunk['metadata']['relative_path']}\n"
            f"{chunk['content']}\n"
            +"="*60
            + "\n\n"
        )
    return context.strip()