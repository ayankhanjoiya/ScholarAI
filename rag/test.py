from dotenv import load_dotenv
load_dotenv()

from google import genai

client = genai.Client()

# from rag.pdf_loader import load_pdf
# from rag.chunker import chunk
# from rag.embeddings import embed_chunks
# from rag.vector_store import add_chunks,collection

# pages = load_pdf("C:\\study material\\ScholarAI\\data\\paper.pdf")
# paper_id = "attention_is_all_you_need"
# title = "Attention Is All You Need"

# chunks = chunk(
#     pages,
#     paper_id,
#     title
# )

# embedded_chunks = embed_chunks(chunks)

# add_chunks(embedded_chunks)

# print("Chunks stored:", collection.count())


from rag.retriever import retrieve

query = "How does BERT use bidirectional context?"

results = retrieve(
    query
)

for i, document in enumerate(results["documents"][0]):

    metadata = results["metadatas"][0][i]

    print(f"\n--- Result {i + 1} ---")
    print("Page:", metadata["page_num"])
    print("Paper ID:", metadata["paper_id"])
    print("Title:",metadata["title"])
    print(document[:500])

# from rag.generator import generate_answer

# answer = generate_answer(
#     client,
#     query,
#     results
# )

# print("\nAnswer:")
# print(answer)

