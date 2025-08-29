import pypdf
import docx

def parse_resume(file):
    text = ""
    name = file.name.lower()
    if name.endswith(".pdf"):
        pdf = pypdf.PdfReader(file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
    return text.strip()
