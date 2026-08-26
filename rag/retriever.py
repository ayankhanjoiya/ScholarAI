from sentence_transformers import SentenceTransformer

from rag.vector_store import search


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, n_results=3):

    query_embedding = model.encode(query).tolist()

    results = search(
        query_embedding,
        n_results=n_results
    )

    return results