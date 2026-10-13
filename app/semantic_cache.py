import redis
import numpy as np

from .embeddings import create_embedding


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)

CACHE_THRESHOLD = 0.35

def store_cache(question: str, answer: str):

    embedding = create_embedding(question)

    redis_client.hset(
        "cache:2",
        mapping={
            "question": question,
            "answer": answer,
            "embedding": np.array(
                embedding,
                dtype=np.float32
            ).tobytes(),
        }
    )

    print("Answer stored in semantic cache.")

def search_cache(query: str):

    query_embedding = create_embedding(query)

    query_vector = np.array(
        query_embedding,
        dtype=np.float32
    ).tobytes()

    results = redis_client.execute_command(
        "FT.SEARCH",
        "semantic_cache_idx",
        "*=>[KNN 1 @embedding $vector AS score]",
        "PARAMS", "2", "vector", query_vector,
        "SORTBY", "score",
        "RETURN", "3", "question", "answer", "score",
        "DIALECT", "2"
    )

    if results[b"total_results"] == 0:
        return None

    result = results[b"results"][0]

    fields = result[b"extra_attributes"]

    score = float(fields[b"score"])

    if score <= CACHE_THRESHOLD:
        return {
            "hit": True,
            "question": fields[b"question"].decode(),
            "answer": fields[b"answer"].decode(),
            "score": score
        }

    return {
        "hit": False,
        "score": score
    }

if __name__ == "__main__":

    query = "Where can I register for the event?"

    result = search_cache(query)

    print(result)