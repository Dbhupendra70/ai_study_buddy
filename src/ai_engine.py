# src/ai_engine.py

import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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

        # 🛡️ CRITICAL: Check if response has valid content before accessing .text
        if not response.candidates:
            logging.error(f"No candidates returned for prompt: {prompt[:200]}...")
            return "⚠️ AI Error: No response generated. Please try again."
        
        if not response.candidates[0].content.parts:
            logging.error(f"No content parts in response for prompt: {prompt[:200]}...")
            return "⚠️ AI Error: No content generated. Try rephrasing your question."

        return response.text.strip()

    except Exception as e:
        logging.error(f"API Error for prompt: {prompt[:200]} | Error: {e}")
        return f"⚠️ AI Error: {str(e)}"
