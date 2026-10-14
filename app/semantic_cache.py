import uuid

import numpy as np
import redis

from .embeddings import create_embedding


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False,
)

CACHE_THRESHOLD = 0.35
CACHE_TTL_SECONDS = 86400  # 24 hours


def store_cache(question: str, answer: str) -> None:
    """Store a question, its answer, and its embedding with a unique key."""

    embedding = create_embedding(question)
    cache_key = f"cache:{uuid.uuid4().hex}"

    redis_client.hset(
        cache_key,
        mapping={
            "question": question,
            "answer": answer,
            "embedding": np.asarray(
                embedding,
                dtype=np.float32,
            ).tobytes(),
        },
    )

    redis_client.expire(cache_key, CACHE_TTL_SECONDS)
    print(f"Answer stored in semantic cache: {cache_key}")


def search_cache(query: str):
    """Return a cached answer when the closest query is within the threshold."""

    query_embedding = create_embedding(query)

    query_vector = np.asarray(
        query_embedding,
        dtype=np.float32,
    ).tobytes()

    results = redis_client.execute_command(
        "FT.SEARCH",
        "semantic_cache_idx",
        "*=>[KNN 1 @embedding $vector AS score]",
        "PARAMS", "2", "vector", query_vector,
        "SORTBY", "score",
        "RETURN", "3", "question", "answer", "score",
        "DIALECT", "2",
    )

    # Handle an empty result set.
    if not results.get(b"results"):
        return None

    result = results[b"results"][0]
    fields = result[b"extra_attributes"]

    score = float(fields[b"score"])

    if score <= CACHE_THRESHOLD:
        return {
            "hit": True,
            "question": fields[b"question"].decode(),
            "answer": fields[b"answer"].decode(),
            "score": score,
        }

    return {
        "hit": False,
        "score": score,
    }


if __name__ == "__main__":
    query = "Where can I register for the event?"
    print(search_cache(query))
