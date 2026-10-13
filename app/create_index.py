import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)

index_name = "semantic_cache_idx"
prefix = "cache:"

try:
    redis_client.execute_command(
        "FT.CREATE",
        index_name,
        "ON", "HASH",
        "PREFIX", "1", prefix,
        "SCHEMA",
        "question", "TEXT",
        "answer", "TEXT",
        "embedding", "VECTOR", "HNSW", "6",
        "TYPE", "FLOAT32",
        "DIM", "384",
        "DISTANCE_METRIC", "COSINE"
    )

    print("Vector index created successfully.")

except redis.exceptions.ResponseError as e:
    print("Index creation failed:", e)