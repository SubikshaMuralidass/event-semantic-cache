from .rag_retriever import search_documents
from .context_builder import build_context
from .llm import generate_answer


def answer_question(question: str) -> str:
    # 1. Retrieve relevant documents
    documents = search_documents(question)

    # 2. Build context
    context = build_context(documents)

    # 3. Generate answer using the context
    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":

    question = "What time does the Redis session start?"

    answer = answer_question(question)

    print("\n--- Answer ---")
    print(answer)