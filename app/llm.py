def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer using the retrieved event context.
    """

    prompt = f"""
You are an event assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I don't have enough information in the event documents."

Context:
{context}

Question:
{question}

Answer:
"""

    # Temporary implementation.
    # Replace this with the actual LLM API call.
    return "LLM integration will be added here."

if __name__ == "__main__":

    context = """
    The Redis for High-Performance Applications session
    starts at 2:00 PM in Hall A.
    """

    question = "When does the Redis session start?"

    answer = generate_answer(question, context)

    print(answer)