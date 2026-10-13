"""
Chunk
  ↓
create_embedding()
  ↓
384-dimensional vector
  ↓
convert to FLOAT32 bytes
  ↓
Redis HASH
"""

import redis
import numpy as np

from .document_loader import load_document
from .chunker import chunk_document
from .embeddings import create_embedding


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=False
)


document = load_document("data/event.md")
chunks = chunk_document(document)

for i, chunk in enumerate(chunks):

    embedding = create_embedding(chunk)

    redis_client.hset(
        f"rag:{i}",
        mapping={
            "text": chunk,
            "embedding": np.array(
                embedding,
                dtype=np.float32
            ).tobytes(),
        }
    )

print(f"Stored {len(chunks)} RAG chunks in Redis.")