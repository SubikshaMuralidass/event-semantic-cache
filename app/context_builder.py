def build_context(documents: list[dict]) -> str:
    """
    Combine retrieved RAG documents into a single context
    that can be provided to the LLM.
    """

    context_parts = []

    for i, document in enumerate(documents, start=1):
        context_parts.append(
            f"[Document {i}]\n{document['text']}"
        )

    return "\n\n".join(context_parts)

if __name__ == "__main__":

    from .rag_retriever import search_documents

    query = "What time does the Redis session start?"

    documents = search_documents(query)

    context = build_context(documents)

    print("\n--- Generated Context ---\n")
    print(context)