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

def retrieve_documents(query : str):
    results = retrieve(query)
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    evidence = []

    for document , metadata in zip(documents,metadatas):
        source = {
            "paper_id": metadata['paper_id'],
            "title": metadata['title'], 
            "page_num": metadata['page_num'],
            "content": document,
        }

        evidence.append(source)

    return evidence