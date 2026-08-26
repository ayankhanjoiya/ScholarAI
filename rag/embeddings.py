from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    texts = []
    for chunk in chunks:
        texts.append(chunk["chunk_text"])
    
    embeddings = model.encode(texts)
        ## used gemini-embedding-001 but api limits :(
    
    for i , chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    return chunks