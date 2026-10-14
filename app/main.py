from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .semantic_cache import search_cache, store_cache
from .rag_pipeline import answer_question

app = FastAPI(
    title="Event Semantic Cache API",
    description="Event Q&A using RAG, Gemini, and Redis semantic caching.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Event Semantic Cache API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    # Step 1: Check the semantic cache.
    cache_result = search_cache(question)

    if cache_result and cache_result["hit"]:
        return {
            "answer": cache_result["answer"],
            "cache": "HIT",
            "similarity_score": cache_result["score"],
        }

    # Step 2: Cache MISS — retrieve context and generate an answer.
    try:
        answer = answer_question(question)

        # Step 3: Store the generated answer for future queries.
        store_cache(question, answer)

    except Exception:
        # Avoid exposing API keys or internal error details.
        raise HTTPException(
            status_code=502,
            detail="Unable to generate an answer. Please try again.",
        )

    return {
        "answer": answer,
        "cache": "MISS",
        "similarity_score": (
            cache_result["score"] if cache_result else None
        ),
    }
