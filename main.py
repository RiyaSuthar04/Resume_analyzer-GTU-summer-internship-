import streamlit as st
from dotenv import load_dotenv
import os
import time
import plotly.graph_objects as go
from utils import extract_text_from_pdf
from agents import analyze_resume, answer_question
from pdf_report import generate_pdf_report  # Import PDF report generator
import tempfile

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App title
st.title("📄 ATS Resume Checker with AI Insights")

# Upload resume
resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("📋 Paste the job description here")

extracted_text = None
if resume_file:
    extracted_text = extract_text_from_pdf(resume_file)

# Trigger resume analysis
if resume_file and job_description:
    with st.expander("🔍 Show extracted resume text"):
        if extracted_text:
            st.text_area("Extracted Resume Text", extracted_text, height=300)
        else:
            st.warning("⚠️ No text could be extracted from the PDF.")

    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing resume with AI agents..."):
            try:
                results, overall_score = analyze_resume(
                    extracted_text, job_description, GEMINI_API_KEY
                )
                st.success("✅ Analysis complete!")
                st.session_state["results"] = results
                st.session_state["overall_score"] = overall_score
                st.session_state["extracted_text"] = extracted_text
                st.session_state["job_description"] = job_description
            except Exception as e:
                st.error(f"❌ Error during resume analysis: {e}")
else:
    st.info("Please upload a PDF resume and paste a job description to begin.")

# Display results
if "results" in st.session_state and "overall_score" in st.session_state:
    st.subheader("📊 ATS Analysis Results")

    st.write(f"### ✅ Overall ATS Score: **{st.session_state['overall_score']} / 10**")
    st.progress(int(st.session_state["overall_score"] * 10))

    # Radar chart
    categories = [k.replace("_", " ").title() for k in st.session_state["results"].keys()]
    scores = [v["score"] for v in st.session_state["results"].values()]

    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill="toself",
        name="Resume Scores"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        title="📌 Agent-wise Resume Score Radar Chart"
    )
    st.plotly_chart(fig)

    # Feedback
    for agent, res in st.session_state["results"].items():
        st.markdown(f"**{agent.replace('_', ' ').title()}**: {res['score']} / 10\n- {res['feedback']}")

    # 💬 Resume Q&A Section
    st.subheader("💬 Ask a question about your resume or job fit")
    with st.form("qa_form"):
        user_question = st.text_input("Your question", key="qa_input")
        submitted = st.form_submit_button("Ask")
        if submitted and user_question.strip():
            with st.spinner("Getting answer from AI..."):
                answer = answer_question(
                    GEMINI_API_KEY,
                    st.session_state["extracted_text"],
                    st.session_state["job_description"],
                    user_question,
                )
            st.markdown(f"**🤖 AI Answer:** {answer}")

    # 📥 PDF Report Download Section
    # 📥 PDF Report Download Section
st.subheader("📥 Download PDF Report")
if st.button("Generate PDF Report"):
    try:
        job_title = st.session_state["job_description"].split("\n")[0][:50]
        candidate_name = resume_file.name.split(".")[0]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            generate_pdf_report(
                output_path=temp.name,
                job_title=job_title,
                candidate_name=candidate_name,
                results_dict=st.session_state["results"],
                overall_score=st.session_state["overall_score"]
            )

            with open(temp.name, "rb") as f:
                pdf_bytes = f.read()

        st.download_button(
            label="📄 Download ATS Report as PDF",
            data=pdf_bytes,
            file_name="ATS_Resume_Report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"❌ Failed to generate PDF report: {e}")

