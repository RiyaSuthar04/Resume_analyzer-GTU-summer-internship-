from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from utils import extract_score_feedback, clean_llm_json_response
import streamlit as st
import json

def get_gemini_llm(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

def agent_prompt(system_message):
    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "Resume:\n{resume_text}\n\nJob Description:\n{job_desc}")
    ])

def run_agent(llm, prompt, resume_text, job_desc, agent_name):
    response = llm.invoke(prompt.format_messages(resume_text=resume_text, job_desc=job_desc))
    try:
        cleaned = clean_llm_json_response(response.content)
        result = json.loads(cleaned)
        if '"score"' in result:
            result['score'] = result.pop('"score"')
        if '"feedback"' in result:
            result['feedback'] = result.pop('"feedback"')
        if 'score' not in result or 'feedback' not in result:
            raise KeyError
    except Exception:
        st.warning(f"Could not parse LLM response for {agent_name} agent. Raw response: {response.content}")
        result = extract_score_feedback(str(response.content))
    return result

def impact_agent(llm, resume_text, job_desc):
    prompt = agent_prompt(
        "You are an expert resume reviewer. Analyze the following resume for impact, focusing on quantifiable achievements, strong action verbs, and results. Compare with the job description. Give a score out of 10 and a short feedback. Respond in JSON: {{\"score\": <score>, \"feedback\": <feedback>}}"
    )
    return run_agent(llm, prompt, resume_text, job_desc, "impact")

def brevity_agent(llm, resume_text, job_desc):
    prompt = agent_prompt(
        "You are an expert resume reviewer. Analyze the following resume for brevity and conciseness. Identify any wordy or redundant sections. Give a score out of 10 and a short feedback. Respond in JSON: {{\"score\": <score>, \"feedback\": <feedback>}}"
    )
    return run_agent(llm, prompt, resume_text, job_desc, "brevity")

def style_agent(llm, resume_text, job_desc):
    prompt = agent_prompt(
        "You are an expert resume reviewer. Analyze the following resume for style, professionalism, and formatting. Note any inconsistencies or issues. Give a score out of 10 and a short feedback. Respond in JSON: {{\"score\": <score>, \"feedback\": <feedback>}}"
    )
    return run_agent(llm, prompt, resume_text, job_desc, "style")

def section_completeness_agent(llm, resume_text, job_desc):
    prompt = agent_prompt(
        "You are an expert resume reviewer. Check if all key sections (Contact, Summary, Experience, Education, Skills) are present and complete. Give a score out of 10 and a short feedback. Respond in JSON: {{\"score\": <score>, \"feedback\": <feedback>}}"
    )
    return run_agent(llm, prompt, resume_text, job_desc, "section completeness")

def analyze_resume(resume_text, job_desc, api_key):
    llm = get_gemini_llm(api_key)
    results = {
        "impact": impact_agent(llm, resume_text, job_desc),
        "brevity": brevity_agent(llm, resume_text, job_desc),
        "style": style_agent(llm, resume_text, job_desc),
        "section_completeness": section_completeness_agent(llm, resume_text, job_desc),
    }
    overall_score = round(sum(r["score"] for r in results.values()) / len(results), 1)
    return results, overall_score

def answer_question(api_key, resume_text, job_desc, user_question):
    llm = get_gemini_llm(api_key)
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert career advisor. Answer the user's question based on the resume and job description provided."),
        ("human", "Resume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\nQuestion: {question}")
    ])
    response = llm.invoke(qa_prompt.format_messages(
        resume_text=resume_text,
        job_desc=job_desc,
        question=user_question
    ))
    return response.content 