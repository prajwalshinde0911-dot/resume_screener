import streamlit as st
from core.ranker import rank_candidates
from core.parser import extract_text
from core.skill_extractor import extract_skills
from core.validator import validate_match
from core.analytics import show_score_chart, show_score_breakdown

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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🔐 Login")
    st.markdown('<p class="subtitle">AI Resume Screening System</p>', unsafe_allow_html=True)

    with st.container(border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.button("Login", type="primary")

        if login_btn:
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.caption("Demo credentials — Username: `admin` | Password: `admin123`")

def dashboard_page():
    # ---------- Sidebar Settings ----------
    with st.sidebar:
        st.header("⚙️ Settings")
        semantic_weight_pct = st.slider("Semantic Match Weight (%)", 0, 100, 60, step=5)
        skill_weight_pct = 100 - semantic_weight_pct
        st.caption(f"Skill Match Weight: {skill_weight_pct}%")

        show_ai_validation = st.checkbox("Show AI Validation (Gemini)", value=True)

        st.divider()
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

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
            df = rank_candidates(
                jd_text,
                uploaded_files,
                semantic_weight=semantic_weight_pct / 100,
                skill_weight=skill_weight_pct / 100
            )

        with st.container(border=True):
            st.subheader("🏆 Candidate Ranking")
            st.dataframe(df, width="stretch")

            csv_data = df.to_csv(index=True).encode("utf-8")
            st.download_button(
                label="⬇️ Download Ranking as CSV",
                data=csv_data,
                file_name="candidate_ranking.csv",
                mime="text/csv"
            )

        with st.container(border=True):
            st.subheader("📊 Analytics")
            tab1, tab2 = st.tabs(["Overall Score", "Score Breakdown"])
            with tab1:
                show_score_chart(df)
            with tab2:
                show_score_breakdown(df)

        with st.container(border=True):
            st.subheader("🔎 Candidate Detail")

            candidate_names = df["Candidate"].tolist()
            selected_name = st.selectbox("Select a candidate to view full details", candidate_names)

            selected_file = next(f for f in uploaded_files if f.name == selected_name)
            selected_file.seek(0)

            resume_text = extract_text(selected_file, selected_file.name)
            resume_skills = extract_skills(resume_text)
            row = df[df["Candidate"] == selected_name].iloc[0]

            colA, colB, colC = st.columns(3)
            colA.metric("Final Score", f"{row['Final Score']}%")
            colB.metric("Semantic Match", f"{row['Semantic Match %']}%")
            colC.metric("Skill Match", f"{row['Skill Match %']}%")

            st.write("**✅ Matched Skills:**", row["Matched Skills"])
            st.write("**⚠️ Missing Skills:**", row["Missing Skills"])
            st.write("**📌 All Extracted Skills:**", ", ".join(resume_skills) if resume_skills else "None detected")

            if show_ai_validation:
                with st.spinner("🤖 Getting AI validation..."):
                    validation = validate_match(jd_text, resume_text)
                st.markdown("**🧠 AI Validation (Powered by Google Gemini):**")
                st.info(validation)

            with st.expander("📄 View Full Resume Text"):
                st.text_area("Extracted content", resume_text, height=250, label_visibility="collapsed")

    elif uploaded_files and not jd_text.strip():
        st.warning("Please paste a Job Description above to rank candidates.")

if st.session_state.logged_in:
    dashboard_page()
else:
    login_page()