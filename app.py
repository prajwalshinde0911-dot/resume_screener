import streamlit as st
from core.parser import extract_text
from core.skill_extractor import extract_skills
from core.matcher import compute_similarity

st.set_page_config(page_title="AI Resume Screening System", layout="wide")
st.title("📄 AI Resume Screening System")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=250)

with col2:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Upload a resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None and jd_text.strip():
    resume_text = extract_text(uploaded_file, uploaded_file.name)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume content", resume_text, height=200)

    skills = extract_skills(resume_text)
    st.subheader("Extracted Skills")
    st.write(", ".join(skills) if skills else "No known skills detected.")

    score = compute_similarity(jd_text, resume_text)
    st.subheader("Match Score")
    st.metric(label="Semantic Match", value=f"{score}%")

elif uploaded_file is not None and not jd_text.strip():
    st.warning("Please paste a Job Description above to calculate a match score.")