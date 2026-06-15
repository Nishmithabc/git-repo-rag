from fastapi import APIRouter
from pydantic import BaseModel
from utils.retriever import retrieve_chunks
from utils.context_builder import build_context
from utils.llm import generate_answer

class QueryRequest(BaseModel):
    repo_name: str
    query: str

router=APIRouter()

SIMIARITY_THRESHOLD = 0.35

@router.post('/query')
async def query_repository(request: QueryRequest):
    retrieved_chunks, retrieved_scores = retrieve_chunks(request.repo_name, request.query, k=3)

    #if nothing is retrieved
    if not retrieved_chunks:
        return{
            "answer": "No relevant information found in the repository for the given query.",
            "sources": []
        }
    
    if retrieved_scores[0] < SIMIARITY_THRESHOLD:
        return{
            "answer": "No relevant information found in the repository for the given query.",
            "sources": []
        }
    #build the context from the retrieved chunks
    context = build_context(retrieved_chunks)

    #send the query and context to the LLM to generate an answer
    answer = generate_answer(question=request.query,context=context)

    return {
    "answer": answer,
    "sources": [
        chunk["metadata"]
        for chunk in retrieved_chunks
    ]
}
