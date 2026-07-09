from utils.llm import client
import json


def generate_repository_summary(chunks):
    """
    Generates a high-level summary of the uploaded repository.
    """

    # Combine chunk contents
    context = "\n\n".join(chunk["content"] for chunk in chunks)

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
        model="llama-3.3-70b-versatile",
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