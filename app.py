import streamlit as st
from core.ranker import rank_candidates
from core.parser import extract_text
from core.skill_extractor import extract_skills

st.set_page_config(page_title="AI Resume Screening System", layout="wide")
st.title("📄 AI Resume Screening System")

st.subheader("Job Description")
jd_text = st.text_area("Paste the Job Description here", height=200)

st.subheader("Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload one or more resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if jd_text.strip() and uploaded_files:
    with st.spinner("Analyzing resumes..."):
        df = rank_candidates(jd_text, uploaded_files)

    st.subheader("🏆 Candidate Ranking")
    st.dataframe(df, use_container_width=True)

    st.subheader("🔍 Candidate Detail")
    candidate_names = df["Candidate"].tolist()
    selected_name = st.selectbox("Select a candidate to view full details", candidate_names)

    # Find the matching uploaded file object
    selected_file = next(f for f in uploaded_files if f.name == selected_name)
    selected_file.seek(0)  # reset file pointer before re-reading

    resume_text = extract_text(selected_file, selected_file.name)
    resume_skills = extract_skills(resume_text)

    row = df[df["Candidate"] == selected_name].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Final Score", f"{row['Final Score']}%")
        st.metric("Semantic Match", f"{row['Semantic Match %']}%")
        st.metric("Skill Match", f"{row['Skill Match %']}%")

    with col2:
        st.write("**Matched Skills:**", row["Matched Skills"])
        st.write("**Missing Skills:**", row["Missing Skills"])

    st.write("**All Extracted Skills:**", ", ".join(resume_skills) if resume_skills else "None detected")

    st.subheader("Full Resume Text")
    st.text_area("Extracted content", resume_text, height=300)

elif uploaded_files and not jd_text.strip():
    st.warning("Please paste a Job Description above to rank candidates.")