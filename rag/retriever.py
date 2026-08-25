from rag.vector_store import search

def retrieve(client,query,n_results=3):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = response.embeddings[0].values

    results = search(
        query_embedding,
        n_results=n_results
    )

    return results