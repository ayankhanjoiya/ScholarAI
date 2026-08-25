def chunk(pages : list):
    chunks = []
    chunk_size = 1000
    overlap = 200
    chunk_id = 0
    for page in pages:
        text = page["text"]
        page_num = page["page"]
        start = 0
        while(start < len(text)):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "page_num":page_num,
                "chunk_id":chunk_id,
                "chunk_text":chunk_text
            })
            chunk_id += 1
            start = start + chunk_size - overlap
    return chunks



