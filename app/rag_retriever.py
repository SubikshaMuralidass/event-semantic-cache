import redis
import numpy as np

from .embeddings import create_embedding


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)


def search_documents(query: str, top_k: int = 3):

    query_embedding = create_embedding(query)

    query_vector = np.array(
        query_embedding,
        dtype=np.float32
    ).tobytes()

    results = redis_client.execute_command(
        "FT.SEARCH",
        "event_rag_idx",
        "*=>[KNN $k @embedding $vector AS score]",
        "PARAMS", "4",
        "k", top_k,
        "vector", query_vector,
        "SORTBY", "score",
        "RETURN", "2",
        "text", "score",
        "DIALECT", "2"
    )

    documents = []

    for result in results[b"results"]:
        fields = result[b"extra_attributes"]

        documents.append({
            "text": fields[b"text"].decode(),
            "score": float(fields[b"score"])
        })

    return documents

if __name__ == "__main__":

    query = "What time does the Redis session start?"

    results = search_documents(query)

    for result in results:
        print("\n--- Result ---")
        print("Score:", result["score"])
        print("Text:", result["text"])