from flask import Flask, request, jsonify
import spacy
import re
import fitz  # PyMuPDF for PDF reading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Clean and normalize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Extract noun/proper noun keywords using spaCy
def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2]

# Extract plain text from PDF
def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Classify keyword relevance
def classify_keywords(resume_text, job_text):
    resume_kw = extract_keywords(clean_text(resume_text))
    job_kw = extract_keywords(clean_text(job_text))

    resume_set = set(resume_kw)
    job_set = set(job_kw)

    matched = resume_set & job_set

    keyword_data = []
    for kw in matched:
        freq_resume = resume_kw.count(kw)
        freq_job = job_kw.count(kw)
        total = freq_resume + freq_job

        # Classify by combined frequency
        if total >= 4:
            relevance = "High"
        elif total == 2 or total == 3:
            relevance = "Moderate"
        else:
            relevance = "Low"

        source = "Both"
        if kw in resume_set and kw not in job_set:
            source = "Resume"
        elif kw in job_set and kw not in resume_set:
            source = "JD"

        keyword_data.append({
            "keyword": kw,
            "relevance": relevance,
            "source": source
        })

    # Match score calculation
    score = len(matched) / len(job_set) * 100 if job_set else 0
    return round(score, 2), keyword_data

# Main route
@app.route('/match', methods=['POST'])
def match_resume():
    resume_file = request.files['resume']
    job_file = request.files['job']

    resume_text = extract_text_from_pdf(resume_file)
    job_text = extract_text_from_pdf(job_file)

    score, keyword_data = classify_keywords(resume_text, job_text)

    return jsonify({
        'score': score,
        'matched_keywords': keyword_data,
        'resume_text': resume_text,
        'job_text': job_text
    })

if __name__ == '__main__':
    app.run(debug=True)
