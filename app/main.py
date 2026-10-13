from fastapi import FastAPI
from pydantic import BaseModel
from .semantic_cache import search_cache, store_cache

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Event Semantic Cache API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):

    # Step 1: Check semantic cache
    cache_result = search_cache(request.question)

    if cache_result and cache_result["hit"]:
        return {
            "answer": cache_result["answer"],
            "cache": "HIT",
            "similarity_score": cache_result["score"]
        }

    # Temporary answer generator
    answer = (
        "This is a temporary answer generated because "
        "the semantic cache did not contain a suitable result."
    )

    # Step 2: Store the generated answer
    store_cache(request.question, answer)

    return {
        "answer": answer,
        "cache": "MISS",
        "similarity_score": cache_result["score"] if cache_result else None
    }