# redis and python connection code here

import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
