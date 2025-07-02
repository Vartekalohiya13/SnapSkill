
import streamlit as st
import spacy
import re

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

def keyword_match_score(resume, job_desc):
    resume_keywords = set(extract_keywords(clean_text(resume)))
    job_keywords = set(extract_keywords(clean_text(job_desc)))

    matches = resume_keywords.intersection(job_keywords)
    score = len(matches) / len(job_keywords) * 100 if job_keywords else 0
    return round(score, 2), matches

# Streamlit UI
st.title("ATS Resume Match Score")
resume_input = st.text_area("Paste your Resume Text")
job_input = st.text_area("Paste the Job Description")

if st.button("Calculate ATS Score"):
    score, matches = keyword_match_score(resume_input, job_input)
    st.subheader(f"✅ ATS Match Score: {score}%")
    st.write("🎯 Matched Keywords:", ", ".join(matches))