import streamlit as st
from core.ranker import rank_candidates
from core.parser import extract_text
from core.skill_extractor import extract_skills
from core.validator import validate_match

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .subtitle {
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: -10px;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetric"] {
        background: #F3F4F6;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.8rem;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Resume Screening System")
st.markdown('<p class="subtitle">Automated candidate screening powered by NLP & semantic AI matching</p>', unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=160, label_visibility="collapsed")

with st.container(border=True):
    st.subheader("📁 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload one or more resumes (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

if jd_text.strip() and uploaded_files:
    with st.spinner("🔍 Analyzing resumes..."):
        df = rank_candidates(jd_text, uploaded_files)

    with st.container(border=True):
        st.subheader("🏆 Candidate Ranking")
        st.dataframe(df, width="stretch")

    with st.container(border=True):
        st.subheader("🔎 Candidate Detail")

        candidate_names = df["Candidate"].tolist()
        selected_name = st.selectbox("Select a candidate to view full details", candidate_names)

        selected_file = next(f for f in uploaded_files if f.name == selected_name)
        selected_file.seek(0)

        resume_text = extract_text(selected_file, selected_file.name)
        resume_skills = extract_skills(resume_text)
        row = df[df["Candidate"] == selected_name].iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Final Score", f"{row['Final Score']}%")
        col2.metric("Semantic Match", f"{row['Semantic Match %']}%")
        col3.metric("Skill Match", f"{row['Skill Match %']}%")

        st.write("**✅ Matched Skills:**", row["Matched Skills"])
        st.write("**⚠️ Missing Skills:**", row["Missing Skills"])
        st.write("**📌 All Extracted Skills:**", ", ".join(resume_skills) if resume_skills else "None detected")

        with st.spinner("🤖 Getting AI validation..."):
            validation = validate_match(jd_text, resume_text)
        st.markdown("**🧠 AI Validation (Powered by Google Gemini):**")
        st.info(validation)

        with st.expander("📄 View Full Resume Text"):
            st.text_area("Extracted content", resume_text, height=250, label_visibility="collapsed")

elif uploaded_files and not jd_text.strip():
    st.warning("Please paste a Job Description above to rank candidates.")