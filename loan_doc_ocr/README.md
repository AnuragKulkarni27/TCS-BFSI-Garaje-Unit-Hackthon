# Medical Data Extraction
OCR project to extract information from personal loan application PDF Documents.

## Demo

https://github.com/abhijeetk597/medical-data-extraction/assets/138308825/3d5d90e8-2858-4831-b1d5-97a3874f256c

## [Click here to see project presentation](https://youtu.be/xh0livz2tSY)

## Overview
Problem Statement: Automated Personal Loan Document Processing
Background:Banks handle numerous personal loan applications, which often require manual data entry and verification from various documents such as ID proofs, income statements, and bank statements. This process is time-consuming and prone to errors. Optical Character Recognition (OCR) technology can automate the extraction of relevant information from these documents, improving efficiency and accuracy.
Objective:Develop an OCR-based solution to automatically extract and process information from personal loan application documents. The system should identify key fields such as applicant name, address, income details, and loan amount. Additionally, the solution should validate the extracted data and integrate with the bank's loan processing system.Requirements:
Data Collection and Preprocessing:
Collect a sample set of personal loan application documents in various formats and qualities.
Preprocess images to enhance text readability (e.g., noise reduction, contrast adjustment).
OCR Implementation:
Use OCR libraries to extract text from personal loan documents.
Develop algorithms to identify and extract key fields from the OCR output.
Data Validation and Integration:
Implement validation checks to ensure the accuracy of extracted data.
Integrate the solution with the bank's loan processing system for seamless data transfer.
User Interface:
Create a user-friendly interface for uploading documents and reviewing extracted data.
Provide options for manual correction of any OCR errors.
Presentation:
Prepare a comprehensive report detailing the methodology, results, and conclusions. Explain why the implemented approach was selected.
You may use streamlit for UI.Submit the recording of the demo with voice over of what has been achieved along with the code.
## <a name="a1">1. Prerequisites</a>
- Install all dependancies from `requirements.txt`
- For `pdf2image` you need to [download `poppler`](https://github.com/belval/pdf2image?tab=readme-ov-file#how-to-install)
- Install Tesseract OCR Engine in your PC
    - [Tesseract installation instrution : Github](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
    - [Tesseract windows specific instructions: Github](https://github.com/UB-Mannheim/tesseract/wiki)
- Set required PATHs as per your environment
### Why this project?
Though I have been learning Data Science, then why am I doing this project? Mainly there are 3 reasons.
01. OCR is a subset of Computer Vision. OCR can be used in an NLP project like summarizing text using LLM.
02. This project involves very fundamental concepts of Python programming like OOP and Modular programming which are industry best practices.
03. Also this project involves creation of a backend server using FastAPI, which is known for its performance and many world-renowned companies such as Uber, Netflix and Microsoft use FastAPI to build their applications.

## <a name="a3">3. Project Execution Steps</a>
- **Step 1:** Convert pdf to image using `pdf2image` library
- **Step 2:** Preprocess the image (Apply `adaptive thresholding and binarization using OpenCV2`)
- **Step 3:** Extracting text from image by passing it through `tesseract OCR engine`
- **Step 4:** Finding useful information from text using `RegEx` and returning in JSON format
- **Step 5:** Creating a `FastAPI backend server` which serves data extraction requests by accepting a pdf_file, file_format and returning a JSON object.
- **Step 6:** To create a Demo of `frontend UI using Streamlit` and connect it with our FastAPI server using Python Requests module.
![Project Execution Steps](8.jpg)

## <a name="a4">4. Code Walkthrough</a>
Explore notebooks and source code of this project.
 - Notebook 1: [Prescription_parser](https://github.com/abhijeetk597/medical-data-extraction/blob/main/Notebooks/01_prescription_parser.ipynb)
 - Notebook 2: [Patient_details_parser](https://github.com/abhijeetk597/medical-data-extraction/blob/main/Notebooks/02_patient_details_parser.ipynb)
 - Backend: [Source code directory](https://github.com/abhijeetk597/medical-data-extraction/tree/main/backend/src)
 - Frontend: [Streamlit app](https://github.com/abhijeetk597/medical-data-extraction/blob/main/frontend/app.py)

## <a name="a5">5. What did I learn through this project?</a>
- How to use OCR for real world projects and key image processing concepts like thresholding using `OpenCV2`.
- Polished up my Python coding skills by using `OOP, code refactoring and modular programming`.
- Setting up of a backend server using `FastAPI` framework.
- Unit testing using `Pytest`.
- How to use `Postman` for API testing.
- I could connect Streamlit frontend with FastAPI backend server using `Python requests` module.

## <a name="a6">6. Challenges faced during this project</a>
- In adapative thresholding, it requires lot of trial and error to reach optimum values of block size and constant.
- Pytest is not properly integrated with VSCode.
- Also I faced path related errors during unit testing even in PyCharm.
- When creating streamlit app, there are very few practical instructions available on internet for connecting it with a backend server and sending files across.

## <a name="a7">7. Directory Structure of Project</a>
```
loan_doc_ocr
├───backend
│   │
│   ├───resources
│   │       pre_1.pdf
│   │       pre_2.pdf
│   │           
│   │
│   ├───src
│   │       extractor.py
│   │       main.py           
│   │       parser_generic.py
│   │       parser_prescription.py
│   │       utils.py
│   │    
│   │
│   └───uploads
│
├───frontend
│       app.py
│
├───Notebooks
│       01_prescription_parser.ipynb
│       02_patient_details_parser.ipynb
│       03_RegEx.ipynb
│   .gitignore
│   README.md
│   requirements.txt
```
