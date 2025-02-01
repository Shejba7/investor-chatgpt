from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF

# Import nltk and download the VADER lexicon (for sentiment analysis)
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Investor ChatGPT API. Visit /docs for API documentation."}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def perform_analysis(extracted_text: str) -> dict:
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(extracted_text)

    # Dummy analysis sections (replace with real logic later)
    return {
        "Key Financial Highlights": (
            "| Metric    | Value  | Explanation |\n"
            "|-----------|--------|-------------|\n"
            "| Revenue   | $500M  | Solid revenue growth observed in recent quarter |"
        ),
        "Business Growth Highlights": (
            "- **Members:** 10,000+ customers\n"
            "- **Products:** 5 major products\n"
            "- **Revenue Mix:** 60% recurring revenue"
        ),
        "Segment Performance": (
            "- **Retail:** Stable performance\n"
            "- **Wholesale:** Growth observed"
        ),
        "Guidance & Future Expectations": "Management expects 10-15% growth next year.",
        "Investor Insights & Risks": (
            "- **Bull Case:** Strong market position, innovative product line\n"
            "- **Bear Case:** Potential competitive pressure from new entrants"
        ),
        "Sentiment Analysis": sentiment_scores,
        "🤖 AI-generated insights": (
            "🤖 Consider focusing on digital transformation initiatives to further drive growth."
        )
    }

@app.post("/analyze/")
async def analyze_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    extracted_text = extract_text_from_pdf(file_bytes)
    analysis = perform_analysis(extracted_text)
    response = {
        "filename": file.filename,
        "extracted_text_preview": extracted_text[:500],
        "analysis": analysis
    }
    return response
