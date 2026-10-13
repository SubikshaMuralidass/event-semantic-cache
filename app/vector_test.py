import redis

from embeddings import create_embedding


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)


question = "What time does the Python workshop start?"

embedding = create_embedding(question)

print("Question:", question)
print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])