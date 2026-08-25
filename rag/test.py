from rag.pdf_loader import load_pdf
from rag.chunker import chunk
from rag.embeddings import embed_chunks

pages = load_pdf("C:\\study material\\ScholarAI\\data\\paper.pdf")
chunks = chunk(pages)

# print("Number of chunks:", len(chunks))

# print("\nFirst chunk:\n")
# print(chunks[0])

# print("\nSecond chunk:\n")
# print(chunks[1])
from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

embedded_chunks = embed_chunks(chunks,client)

print("Number of chunks:", len(embedded_chunks))

print("\nFirst embedded chunk:")
print(embedded_chunks[0]["page_num"])
print(embedded_chunks[0]["chunk_id"])
print(embedded_chunks[0]["chunk_text"][:100])

print("\nFirst 10 embedding values:")
print(embedded_chunks[0]["embedding"][:10])


