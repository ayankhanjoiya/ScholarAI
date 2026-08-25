def generate_answer(client, query, results):

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    prompt = f"""
Answer the question using only the evidence provided below.

If the evidence is insufficient to answer the question, say:
"Insufficient evidence to answer this question."

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