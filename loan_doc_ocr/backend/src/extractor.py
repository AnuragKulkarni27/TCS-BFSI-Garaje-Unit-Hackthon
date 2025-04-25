from pdf2image import convert_from_path
import pytesseract
import utils
from loan_application_document import PrescriptionParser
import os

POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\poppler-24.08.0\Library\bin")
TESSERACT_ENGINE_PATH = os.getenv("TESSERACT_PATH", r"C:/Program Files/Tesseract-OCR/tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_ENGINE_PATH

def extract(file_path, file_format):
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ""

    for page in pages:
        processed_image = utils.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang="eng")
        document_text += "\n" + text

    if file_format == "prescription":
        return PrescriptionParser(document_text).parse()
    else:
        raise Exception(f"Invalid file format: {file_format}")

if __name__ == "__main__":
    data = extract("backend/resources/prescription/pre_1.pdf", "prescription")
    print(data)
