import streamlit as st
import requests
from pdf2image import convert_from_bytes
import ast
import time

POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
URL = "http://127.0.0.1:8000/extract_from_doc"
st.title("Automated Personal Loan Document Processing 📄")
file = st.file_uploader("Upload file", type=["png", "jpg", "jpeg", "pdf"])
col3, col4 = st.columns(2)
with col3:
    file_format = st.radio(label="Document", options=["prescription", "patient_details"], horizontal=True)
with col4:
    if file and st.button("Upload PDF", type="primary"):
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)
        payload = {'file_format': file_format}
        files=[('file', file.getvalue())]
        headers = {}
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
        dict_str = response.content.decode("UTF-8")
        data = ast.literal_eval(dict_str)
        if data:
            st.session_state = data

if file:
    pages = convert_from_bytes(file.getvalue(), poppler_path=POPPLER_PATH)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your file")
        st.image(pages[0])

    with col2:
        if st.session_state:
            st.subheader("Details")
            name = st.text_input(label="Name", value=st.session_state["name"])
            address = st.text_input(label="Address", value=st.session_state["address"])
            income_details = st.text_input(label="Income Details", value=st.session_state["income_details"])
            loan_amount = st.text_input(label="Loan Amount", value=st.session_state["loan_amount"])
            refill = st.text_input(label="refill", value=st.session_state["refill"])
            if st.button(label="Submit", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success('Details successfully recorded.')