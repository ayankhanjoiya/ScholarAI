def generate_answer(client, query, results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    evidence = []

    for document, metadata in zip(documents, metadatas):

        source = (
            f"Paper: {metadata['title']}\n"
            f"Page: {metadata['page_num']}\n"
            f"Evidence: {document}"
        )

        evidence.append(source)

    context = "\n\n---\n\n".join(evidence)

    prompt = f"""
Answer the question using only the evidence provided below.

If the evidence is insufficient to answer the question, say:
"Insufficient evidence to answer this question."

For every factual claim, include a citation in this format:

[Paper Title, p. Page Number]

Question:
{query}

Evidence:
{context}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text