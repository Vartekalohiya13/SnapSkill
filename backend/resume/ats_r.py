# from flask import Flask, request, jsonify
# import spacy
# import re
# import fitz  # PyMuPDF for PDF reading
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load spaCy NLP model
# nlp = spacy.load("en_core_web_sm")

# # Clean and normalize text
# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r'[^\w\s]', '', text)
#     return text

# # Extract noun/proper noun keywords using spaCy
# def extract_keywords(text):
#     doc = nlp(text)
#     return [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2]

# # Extract plain text from PDF
# def extract_text_from_pdf(file):
#     with fitz.open(stream=file.read(), filetype="pdf") as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()
#     return text

# # Classify keyword relevance
# def classify_keywords(resume_text, job_text):
#     resume_kw = extract_keywords(clean_text(resume_text))
#     job_kw = extract_keywords(clean_text(job_text))

#     resume_set = set(resume_kw)
#     job_set = set(job_kw)

#     matched = resume_set & job_set

#     keyword_data = []
#     for kw in matched:
#         freq_resume = resume_kw.count(kw)
#         freq_job = job_kw.count(kw)
#         total = freq_resume + freq_job

#         # Classify by combined frequency
#         if total >= 4:
#             relevance = "High"
#         elif total == 2 or total == 3:
#             relevance = "Moderate"
#         else:
#             relevance = "Low"

#         source = "Both"
#         if kw in resume_set and kw not in job_set:
#             source = "Resume"
#         elif kw in job_set and kw not in resume_set:
#             source = "JD"

#         keyword_data.append({
#             "keyword": kw,
#             "relevance": relevance,
#             "source": source
#         })

#     # Match score calculation
#     score = len(matched) / len(job_set) * 100 if job_set else 0
#     return round(score, 2), keyword_data

# # Main route
# @app.route('/match', methods=['POST'])
# def match_resume():
#     resume_file = request.files.get('resume')

#     if not resume_file:
#         return jsonify({"error": "No resume file uploaded."}), 400

#     # ✅ Use default JD text (or a static PDF you load once)
#     default_job_text = """
#     We are looking for a Software Engineer with experience in Python, APIs, cloud (AWS/Azure),
#     frontend frameworks like React, and good communication skills. Familiarity with CI/CD and Git is a plus.
#     """

#     resume_text = extract_text_from_pdf(resume_file)
#     job_text = default_job_text

#     score, keyword_data = classify_keywords(resume_text, job_text)

#     return jsonify({
#         'score': score,
#         'matched_keywords': keyword_data,
#         'resume_text': resume_text,
#         'job_text': job_text
#     })


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
import spacy
import re
import fitz  # PyMuPDF for PDF reading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load spaCy model with lemmatization
nlp = spacy.load("en_core_web_sm")

# ✅ Clean and normalize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# ✅ Extract lemmatized keywords using spaCy (nouns + verbs + proper nouns)
def extract_keywords(text):
    doc = nlp(text)
    keywords = [
        token.lemma_ for token in doc
        if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and len(token.text) > 2
    ]
    return keywords

# ✅ Extract text from PDF
def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# ✅ Classify keyword overlap + relevance
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

        relevance = "Low"
        if total >= 4:
            relevance = "High"
        elif total == 2 or total == 3:
            relevance = "Moderate"

        keyword_data.append({
            "keyword": kw,
            "relevance": relevance,
            "source": "Both"
        })

    # ✅ Score calculation
    score = (len(matched) / len(job_set) * 100) if job_set else 0
    return round(score, 2), keyword_data

# ✅ Main endpoint
@app.route('/match', methods=['POST'])
def match_resume():
    resume_file = request.files.get('resume')

    if not resume_file:
        return jsonify({"error": "No resume uploaded"}), 400

    # ✅ Default job description
    job_description = """
    We are hiring a software engineer skilled in Python, REST APIs, cloud technologies (AWS/Azure),
    CI/CD, React frontend, and Git. Strong problem-solving and communication skills preferred.
    """

    # Extract texts
    resume_text = extract_text_from_pdf(resume_file)
    job_text = job_description

    score, keyword_data = classify_keywords(resume_text, job_text)

    return jsonify({
        "score": score,
        "matched_keywords": keyword_data,
        "resume_text": resume_text[:1000],
        "job_text": job_text
    })

if __name__ == "__main__":
    app.run(debug=True)
