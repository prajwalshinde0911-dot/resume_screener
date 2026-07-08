import pdfplumber
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from a PDF file (Streamlit uploaded file or path)."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file):
    """Extract text from a DOCX file (Streamlit uploaded file or path)."""
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_text(file, filename):
    """Route to the right extractor based on file extension."""
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
    