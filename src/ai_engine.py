# src/ai_engine.py

import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

def get_gemini_api_key():
    # First: try Streamlit Cloud secrets (deployment)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        pass

    # Fallback: local .env (development)
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "Gemini API key not found. "
            "Add to .env (local) or Streamlit Secrets (cloud)."
        )
    return key

def generate_text(prompt: str) -> str:
    try:
        genai.configure(api_key=get_gemini_api_key())
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=2000,
                temperature=0.7,
            ),
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
