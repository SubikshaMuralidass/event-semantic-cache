import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)

index_name = "event_rag_idx"
prefix = "rag:"

try:
    redis_client.execute_command(
        "FT.CREATE",
        index_name,
        "ON", "HASH",
        "PREFIX", "1", prefix,
        "SCHEMA",
        "text", "TEXT",
        "embedding", "VECTOR", "HNSW", "6",
        "TYPE", "FLOAT32",
        "DIM", "384",
        "DISTANCE_METRIC", "COSINE"
    )

    print("RAG vector index created successfully.")

except redis.exceptions.ResponseError as e:
    print("Index creation failed:", e)