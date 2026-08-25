def embed_chunks(chunks,client):
    texts = []
    for chunk in chunks:
        texts.append(chunk["chunk_text"])
    response = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = texts
    )
    for i , chunk in enumerate(chunks):
        chunk["embedding"] = response.embeddings[i].values

    return chunks