import fitz

def load_pdf(pdf_path : str):
    document = fitz.open(pdf_path)

    pages = []

    for page_num , page in enumerate(document):
        text = page.get_text()

        pages.append({
            "page": page_num + 1,
            "text": text
        })

    return pages