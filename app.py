import streamlit as st
from core.parser import extract_text

st.set_page_config(page_title="AI Resume Screening System", layout="wide")
st.title("📄 AI Resume Screening System")

uploaded_file = st.file_uploader("Upload a resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    text = extract_text(uploaded_file, uploaded_file.name)
    st.subheader("Extracted Text")
    st.text_area("Resume content", text, height=400)
    