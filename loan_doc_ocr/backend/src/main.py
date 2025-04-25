from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from pdf2image import convert_from_bytes
import re
from typing import Optional
import os
import logging
from pydantic import BaseModel
import traceback

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = ["*"]  # Allow all origins for testing

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration - Update these paths
POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\poppler-24.08.0\Library\bin")
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class ExtractionResponse(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    income: Optional[str] = None
    loan_amount: Optional[str] = None

def clean_text(text: str) -> str:
    """Normalize text for better pattern matching"""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\(\d{3}\) \d{3}-\d{4}', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def extract_from_text(text: str) -> dict:
    """Improved extraction for loan documents"""
    extracted = {
        "name": None,
        "address": None,
        "income": None,
        "loan_amount": None
    }
    
    try:
        # Clean the text
        text = clean_text(text)
        
        # Extract Name - more precise pattern
        name_match = re.search(r'(?i)(?:name:\s*)([^\n]+)', text)
        if name_match:
            extracted["name"] = name_match.group(1).strip()
        
        # Extract Address - handle multi-line
        address_match = re.search(r'(?i)(?:address:\s*)([^\n]+)', text)
        if address_match:
            extracted["address"] = address_match.group(1).strip()
        
        # Extract Income - handle different formats
        income_match = re.search(r'(?i)(?:income details?|annual income)[:\s]*([\d,]+)', text)
        if income_match:
            extracted["income"] = income_match.group(1).strip() + "/-"
        else:
            # Fallback to any amount that looks like income
            amounts = re.findall(r'(\d{1,3}(?:,\d{3})+)', text)
            if len(amounts) > 1:  # Assuming income is the second largest amount
                extracted["income"] = amounts[-2] + "/-"
        
        # Extract Loan Amount - specific pattern
        loan_match = re.search(r'(?i)(?:loan amounts?)[:\s]*([\d,]+)', text)
        if loan_match:
            extracted["loan_amount"] = loan_match.group(1).strip() + "/-"
        else:
            # Fallback to largest amount
            amounts = re.findall(r'(\d{1,3}(?:,\d{3})+)', text)
            if amounts:
                extracted["loan_amount"] = amounts[-1] + "/-"
        
        return extracted
    
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}\n{traceback.format_exc()}")
        return extracted

@app.post("/extract_from_doc", response_model=ExtractionResponse)
async def extract(
    file: UploadFile = File(...),
    file_format: Optional[str] = Form("file")
):
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file provided")

        try:
            images = convert_from_bytes(content, poppler_path=POPPLER_PATH)
            if not images:
                raise HTTPException(status_code=400, detail="PDF conversion failed")
            
            text = pytesseract.image_to_string(images[0])
            logger.info(f"Extracted text:\n{text}")
            
            extracted_data = extract_from_text(text)
            logger.info(f"Extracted data: {extracted_data}")
            
            return extracted_data

        except pytesseract.TesseractError as e:
            logger.error(f"OCR Error: {str(e)}")
            raise HTTPException(status_code=500, detail="OCR processing failed")
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)