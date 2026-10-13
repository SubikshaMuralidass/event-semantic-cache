def chunk_document(document: str):

    sections = document.split("\n## ")

    chunks = []

    for section in sections:

        section = section.strip()

        if not section:
            continue

        if section.startswith("Sessions\n"):
            sessions_text = section[len("Sessions\n"):].strip()

            sessions = sessions_text.split("\n### ")

            for session in sessions:

                session = session.strip()

                if not session:
                    continue

                if not session.startswith("###"):
                    session = "### " + session

                chunks.append("## Sessions\n\n" + session)

        else:

            if not section.startswith("#"):
                section = "## " + section

            chunks.append(section)

    return chunks


if __name__ == "__main__":

    from .document_loader import load_document

    document = load_document("data/event.md")

    chunks = chunk_document(document)

    print("Number of chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)