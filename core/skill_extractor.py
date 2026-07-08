import re

SKILLS_DB = [
    "python", "java", "c++", "javascript", "sql", "html", "css",
    "machine learning", "deep learning", "data science", "nlp",
    "natural language processing", "streamlit", "flask", "django",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "spacy", "excel", "power bi", "tableau", "aws", "azure", "gcp",
    "docker", "kubernetes", "git", "github", "rest api", "react",
    "node.js", "mongodb", "mysql", "postgresql", "communication",
    "leadership", "teamwork", "problem solving"
]

def extract_skills(text):
    """Extract skills from text using whole-word/phrase matching."""
    text_lower = text.lower()

    found_skills = set()
    for skill in SKILLS_DB:
        # Escape special regex characters like C++, and match whole word/phrase
        pattern = r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(found_skills)