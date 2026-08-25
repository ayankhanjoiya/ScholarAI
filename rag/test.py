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

from rag.retriever import retrieve

query = "What programming language was used to implement the Transformer?"

results = retrieve(
    client,
    query
)

# for i, document in enumerate(results["documents"][0]):

#     metadata = results["metadatas"][0][i]

#     print(f"\n--- Result {i + 1} ---")
#     print("Page:", metadata["page_num"])
#     print("Chunk ID:", metadata["chunk_id"])
#     print(document[:500])

from rag.generator import generate_answer

answer = generate_answer(
    client,
    query,
    results
)

print("\nAnswer:")
print(answer)

