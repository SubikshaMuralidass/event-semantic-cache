import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_answer(question: str, context: str) -> str:
    """Generate a grounded answer using the Gemini API."""

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    prompt = f"""
You are a helpful TechConnect 2026 event assistant.

Instructions:
- Answer using only the event context below.
- Do not invent dates, times, speakers, locations, or other facts.
- If the answer is not in the context, say:
  "I don't have enough information in the event documents."
- Keep the answer clear and concise.

Event context:
{context}

User question:
{question}

Answer:
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    answer = response.text

    if not answer or not answer.strip():
        raise RuntimeError("Gemini returned an empty response.")

    return answer.strip()


if __name__ == "__main__":
    context = """
    The Redis for High-Performance Applications session
    starts at 2:00 PM in Hall A.
    """

    question = "When does the Redis session start?"

    print(generate_answer(question, context))
