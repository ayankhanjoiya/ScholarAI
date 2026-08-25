# from rag.pdf_loader import load_pdf
# from rag.chunker import chunk
# from rag.embeddings import embed_chunks
# from rag.vector_store import add_chunks,collection

# pages = load_pdf("C:\\study material\\ScholarAI\\data\\paper.pdf")
# chunks = chunk(pages)

from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

# embedded_chunks = embed_chunks(chunks,client)

# add_chunks(embedded_chunks)

# print("Chunks stored:", collection.count())

query = "What architecture does the paper propose?"

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_embedding = response.embeddings[0].values

from rag.vector_store import search

results = search(query_embedding)

for i, document in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    print(f"\n--- Result {i + 1} ---")
    print(document[:500])
    print("Page:", metadata["page_num"])
    print("Chunk ID:", metadata["chunk_id"])

