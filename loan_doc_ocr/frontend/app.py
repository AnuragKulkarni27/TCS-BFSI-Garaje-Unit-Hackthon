import streamlit as st
import requests
from pdf2image import convert_from_bytes
import os
import time

POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\poppler-24.08.0\Library\bin")
BACKEND_URL = "http://localhost:8000/extract_from_doc"

# Page setup
st.set_page_config(page_title="Loan Doc Processor", layout="wide")
st.title("Loan Application Processor")
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'error' not in st.session_state:
    st.session_state.error = None

# File upload
uploaded_file = st.file_uploader("Upload Loan Document", type=["pdf"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Document Preview")
        try:
            pages = convert_from_bytes(uploaded_file.getvalue(), poppler_path=POPPLER_PATH)
            st.image(pages[0], use_container_width=True)
        except Exception as e:
            st.error(f"Preview error: {str(e)}")
    
    with col2:
        st.subheader("Extracted Information")
        
        if st.button("Extract Data", type="primary"):
            with st.spinner("Processing document..."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                    response = requests.post(BACKEND_URL, files=files)
                    
                    if response.status_code == 200:
                        st.session_state.extracted_data = response.json()
                        st.success("Data extracted successfully!")
                    else:
                        st.session_state.error = response.json().get('detail', 'Extraction failed')
                        st.error(st.session_state.error)
                except Exception as e:
                    st.session_state.error = f"Connection error: {str(e)}"
                    st.error(st.session_state.error)
        
        if st.session_state.error:
            st.error(st.session_state.error)
        
        if st.session_state.extracted_data:
            data = st.session_state.extracted_data
            
            with st.form("loan_form"):
                st.markdown("### Verify Extracted Details")
                
                cols = st.columns(2)
                with cols[0]:
                    name = st.text_input("Full Name", value=data.get("name", ""))
                    address = st.text_area("Address", value=data.get("address", ""), height=100)
                with cols[1]:
                    income = st.text_input("Annual Income", value=data.get("income", "7,00,000/-"))
                    loan_amount = st.text_input("Loan Amount", value=data.get("loan_amount", "20,00,000/-"))
                
                if st.form_submit_button("Submit Application"):
                    if not name or not address:
                        st.error("Name and Address are required")
                    else:
                        st.success("Application submitted!")
                        st.session_state.extracted_data = None
                        time.sleep(2)
                        st.rerun()
