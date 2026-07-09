import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def validate_match(jd_text, resume_text):
    """Ask Gemini to independently score the match as a validation check."""
    prompt = f"""You are an expert recruiter. Compare this Job Description and Resume.
Give a match score from 0-100 based on how well the candidate fits the role,
and a 2-line reason for the score.

Job Description:
{jd_text}

Resume:
{resume_text}

Respond in this exact format:
Score: <number>
Reason: <your reasoning in 2 lines>
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text