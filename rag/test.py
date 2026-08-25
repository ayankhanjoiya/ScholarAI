from rag.pdf_loader import load_pdf
from rag.chunker import chunk
from rag.embeddings import embed_chunks
from rag.vector_store import add_chunks,collection

pages = load_pdf("C:\\study material\\ScholarAI\\data\\paper.pdf")
chunks = chunk(pages)

from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

embedded_chunks = embed_chunks(chunks,client)

add_chunks(embedded_chunks)

print("Chunks stored:", collection.count())


