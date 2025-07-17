import streamlit as st
from dotenv import load_dotenv
import os
from utils import extract_text_from_pdf
from agents import analyze_resume, answer_question

# --- Streamlit UI ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.title("ATS Resume Checker")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the job description here")

extracted_text = None
if resume_file:
    extracted_text = extract_text_from_pdf(resume_file)

if resume_file and job_description:
    with st.expander("Show extracted resume text"):
        if extracted_text:
            st.text_area("Extracted Resume Text", extracted_text, height=300)
        else:
            st.warning("No text could be extracted from the PDF.")
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume with AI agents..."):
            import time
            start_time = time.time()
            results, overall_score = analyze_resume(extracted_text, job_description, GEMINI_API_KEY)
            elapsed = time.time() - start_time
            if elapsed > 25:
                st.info("This is taking longer than usual. Please wait...")
        st.session_state['results'] = results
        st.session_state['overall_score'] = overall_score
        st.session_state['extracted_text'] = extracted_text
        st.session_state['job_description'] = job_description

if 'results' in st.session_state and 'overall_score' in st.session_state:
    st.subheader("ATS Analysis Results")
    st.write(f"**Overall ATS Score:** {st.session_state['overall_score']} / 10")
    for agent, res in st.session_state['results'].items():
        st.markdown(f"**{agent.replace('_', ' ').title()}**: {res['score']} / 10\n- {res['feedback']}")

    st.subheader("Ask a question about your resume or job fit")
    with st.form("qa_form"):
        user_question = st.text_input("Your question", key="qa_input")
        submitted = st.form_submit_button("Ask")
        if submitted and user_question.strip():
            with st.spinner("Getting answer from AI..."):
                answer = answer_question(
                    GEMINI_API_KEY,
                    st.session_state['extracted_text'],
                    st.session_state['job_description'],
                    user_question
                )
            st.markdown(f"**AI Answer:** {answer}")
else:
    st.write("Please upload your resume and enter a job description.")
