from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF

app = FastAPI()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)
    return {"filename": file.filename, "extracted_text": extracted_text[:500]}
