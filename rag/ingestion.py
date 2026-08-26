papers = [
    {
        "path" : "C:\study material\ScholarAI\data\paper.pdf",
        "paper_id": "attention_is_all_you_need",
        "title":"Attention Is All You Need",
    },
    {
        "path" : "C:\\study material\\ScholarAI\\data\\bert.pdf",
        "paper_id": "bert_pretraining",
        "title":"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
    }
]

from rag.pdf_loader import load_pdf
from rag.chunker import chunk
from rag.embeddings import embed_chunks
from rag.vector_store import add_chunks, collection

for paper in papers:

    print(f"\nProcessing: {paper['title']}")

    pages = load_pdf(paper["path"])

    chunks = chunk(
        pages,
        paper["paper_id"],
        paper["title"]
    )

    embedded_chunks = embed_chunks(chunks)

    add_chunks(embedded_chunks)

    print(f"Stored {len(chunks)} chunks")

print("\nTotal chunks in database:", collection.count())