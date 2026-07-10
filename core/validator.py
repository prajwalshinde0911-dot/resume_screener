import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)