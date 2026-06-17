from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

client = Groq(
    api_key=api_key
)

def generate_answer(question: str, context: str):

    prompt = f"""
You are an AI assistant that answers questions about a GitHub repository.

Use ONLY the provided repository context.
Explain the code in a concise and developer-friendly manner.
If the answer cannot be found in the context, reply exactly:
"No relevant information was found in the uploaded repository for this question."
Do not use outside knowledge."

Repository Context:
-------------------
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
