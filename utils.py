import streamlit as st
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(resume_file):
    try:
        pdf_reader = PdfReader(resume_file)
        return "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def extract_score_feedback(text):
    score_match = re.search(r'score\s*[:=\-]?\s*(\d+)', text, re.IGNORECASE)
    feedback_match = re.search(r'feedback\s*[:=\-]?\s*([\s\S]+)', text, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0
    feedback = feedback_match.group(1).strip() if feedback_match else "Could not extract feedback."
    return {"score": score, "feedback": feedback}

def clean_llm_json_response(text):
    text = text.strip()
    if text.startswith('```'):
        lines = text.splitlines()
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        text = '\n'.join(lines)
    return text 