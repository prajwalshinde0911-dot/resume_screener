import pandas as pd
from core.parser import extract_text
from core.skill_extractor import extract_skills
from core.matcher import compute_similarity

def rank_candidates(jd_text, uploaded_files):
    """Process multiple resumes and return a ranked DataFrame."""
    results = []

    jd_skills = set(extract_skills(jd_text))

    for file in uploaded_files:
        resume_text = extract_text(file, file.name)
        resume_skills = set(extract_skills(resume_text))

        semantic_score = compute_similarity(jd_text, resume_text)

        # Skill match: how many JD skills are found in the resume
        if jd_skills:
            skill_match_pct = round(len(resume_skills & jd_skills) / len(jd_skills) * 100, 2)
        else:
            skill_match_pct = 0.0

        # Final score: weighted combination
        final_score = round(0.6 * semantic_score + 0.4 * skill_match_pct, 2)

        missing_skills = jd_skills - resume_skills

        results.append({
            "Candidate": file.name,
            "Final Score": final_score,
            "Semantic Match %": semantic_score,
            "Skill Match %": skill_match_pct,
            "Matched Skills": ", ".join(sorted(resume_skills & jd_skills)) or "-",
            "Missing Skills": ", ".join(sorted(missing_skills)) or "-",
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Final Score", ascending=False).reset_index(drop=True)
    df.index += 1  # rank starts at 1
    return df
