import os, pdfplumber, docx2txt

def load_text_from_pdf(path:str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text.append(t)
    return "\n".join(text)

def load_text_from_docx(path:str) -> str:
    return docx2txt.process(path) or ""

def load_text_from_path(path:str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return load_text_from_pdf(path)
    if ext in [".docx", ".doc"]:
        return load_text_from_docx(path)
    raise ValueError(f"Formato no soportado: {ext}")