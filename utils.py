import streamlit as st
from PyPDF2 import PdfReader
import re

import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"


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