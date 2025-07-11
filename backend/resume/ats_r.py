from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import spacy

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")

# Dummy JD text for comparison (you can replace with a real one)
JOB_DESCRIPTION = """
We are looking for a Python developer with experience in Flask, REST APIs, 
machine learning, and teamwork. Knowledge of NLP is a plus.
"""

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "".join(page.get_text() for page in doc)

def extract_keywords(text):
    doc = nlp(text.lower())
    return list(set([token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ", "VERB")]))

@app.route("/match", methods=["POST"])
def match_resume():
    resume = request.files.get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded"}), 400

    resume_text = extract_text_from_pdf(resume)
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(JOB_DESCRIPTION)

    matched = list(set(resume_keywords) & set(jd_keywords))
    missing = list(set(jd_keywords) - set(resume_keywords))

    score = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

    return jsonify({
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing
    })

if __name__ == "__main__":
    app.run(debug=True)
