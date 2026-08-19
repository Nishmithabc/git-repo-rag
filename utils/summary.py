from utils.llm import client
import json

def _condense_chunks(chunks, char_budget=10000):
    """
    Reduces chunk content to fit within a safe token budget.
    Strategy: if chunks already fit, use them as-is.
    Otherwise, do a cheap per-file/per-chunk truncation pass
    so every part of the repo is still represented, just shorter.
    """
    full_context = "\n\n".join(chunk["content"] for chunk in chunks)

    # Roughly 4 chars/token — keep this comfortably under the TPM limit,
    # leaving headroom for the prompt template text + model output.
    if len(full_context) <= char_budget:
        return full_context

    # Repo is too big to fit raw — take a proportional slice from each chunk
    # instead of just cutting off the tail, so every file gets some representation.
    per_chunk_budget = max(char_budget // len(chunks), 200)
    trimmed = []
    for chunk in chunks:
        content = chunk["content"]
        if len(content) > per_chunk_budget:
            content = content[:per_chunk_budget] + "\n...[truncated]"
        trimmed.append(content)

    return "\n\n".join(trimmed)

def generate_repository_summary(chunks):
    """
    Generates a high-level summary of the uploaded repository.
    """

    # Combine chunk contents
    context = _condense_chunks(chunks)

    prompt = f"""
You are an expert software engineer.

Analyze the following GitHub repository and produce a professional repository overview.

Format your response using Markdown.

Use the following structure exactly:
---

 📦 Repository Overview

🎯 Purpose
Write 2-3 concise sentences explaining what the project is and what problem it solves.

🛠️ Technology Stack
Group technologies into categories.

Example:
- Languages: Python
- Frontend: React, Streamlit
- Backend: FastAPI
- AI/ML: FAISS, Sentence Transformers, Llama
- Database: PostgreSQL
- Other Tools: Docker, Git

⚙️ Project Workflow

Represent the workflow using arrows.

Example:

User Uploads File
↓
Data Processing
↓
Embedding Generation
↓
Vector Search
↓
LLM Response

📂 Key Modules

Present this as a table.

| Module | Responsibility |
|--------|----------------|
| main.py | Starts the application |
| routes/ | API endpoints |
| utils/ | Helper functions |

Only include important modules.

✨ Key Features

Use bullet points.

Example:
- Semantic code search
- Repository summarization
- Retrieval-Augmented Generation
- AI-powered question answering

💡 Overall Architecture

Briefly explain how the different modules interact in one paragraph.
---
Guidelines:
- Keep the response under 350 words.
- Be concise and professional.
- Do not mention technologies that are not present in the repository.
- Infer architecture only from the repository contents.
- Do not invent features.

Repository Content:

{context}
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You summarize software repositories."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content