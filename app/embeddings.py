# using sentence-transformers and the all-MiniLM-L6-v2 model to generate embeddings for a given text

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text: str):
    return model.encode(text).tolist()