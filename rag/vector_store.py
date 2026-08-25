import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="research_papers"
)

def add_chunks(chunks):
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        ids.append(f"chunk_{chunk['chunk_id']}")

        documents.append(chunk['chunk_text'])

        embeddings.append(chunk['embedding'])

        metadatas.append({
            "page_num" : chunk["page_num"],
            "chunk_id" : chunk["chunk_id"],
        })

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
    
def search(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results

    