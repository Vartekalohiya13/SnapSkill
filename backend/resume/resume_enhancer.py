from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import base64
import io
import os
import json
from dotenv import load_dotenv

print("💡 Running resume_enhancer.py...")

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Confirm key
cohere_key = os.getenv("COHERE_API_KEY")
print("🔐 Loaded Cohere Key:", cohere_key[:8] + "..." if cohere_key else "❌ No API key found!")

# LangChain: use Cohere
from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate

app = Flask(__name__)
CORS(app)

# LangChain LLM setup
llm = ChatCohere(model="command", temperature=0.5, cohere_api_key=cohere_key)

# PDF text extraction
def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

# LLM-enhanced resume

def get_suggestions_and_enhanced_resume(text):
    prompt = PromptTemplate(
        input_variables=["resume"],
        template="""

You are an expert resume coach and professional resume writer.

Given this raw resume text:

{resume}

Your tasks:
1. Write 3-5 clear, concise, actionable suggestions to improve this resume for Applicant Tracking Systems (ATS) and impact.
2. Rewrite the resume in a professional, ATS-optimized, modern format. Ensure it's:
   - In a clean structure (e.g., Name, Summary, Experience, Education, Skills).
   - Well-aligned.
   - Keyword-rich and uses bullet points for experience.
   - Ideally 1-page length.

Please return the result in this format:

Suggestions:
1. ...
2. ...
3. ...

Enhanced Resume:
Name: John Doe
Email: john@example.com
Phone: +1-555-123-4567
LinkedIn: linkedin.com/in/johndoe

Summary:
A brief 2–3 sentence professional summary...

Experience:
- Job Title, Company (Dates)
  • Achievement or responsibility
  • Achievement or responsibility

Education:
- Degree, Institution, Year

Skills:
- Skill 1, Skill 2, Skill 3
"""

    )

    chain = prompt | llm
    response = chain.invoke({"resume": text})
    content = response.content.strip()

    # Fallback parser
    try:
        suggestions_part = content.split("Enhanced Resume:")[0]
        resume_part = content.split("Enhanced Resume:")[1]

        # Extract numbered suggestions from text
        suggestions = [
            line.strip()
            for line in suggestions_part.splitlines()
            if line.strip().startswith(tuple("123456789"))
        ]
        enhanced_text = resume_part.strip()

    except Exception as e:
        print("❌ Fallback parsing failed:", e)
        suggestions = ["Could not parse suggestions."]
        enhanced_text = "Error generating enhanced resume."

    return suggestions, enhanced_text

def create_pdf_from_text(text):
    pdf_io = io.BytesIO()
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=11)
    doc.save(pdf_io)
    doc.close()
    return pdf_io.getvalue()

@app.route("/enhance", methods=["POST"])
def enhance_resume():
    resume_file = request.files.get("resume")
    if not resume_file:
        return jsonify({"error": "No resume uploaded"}), 400

    try:
        resume_text = extract_text_from_pdf(resume_file)
        suggestions, enhanced_resume_text = get_suggestions_and_enhanced_resume(resume_text)
        enhanced_pdf = create_pdf_from_text(enhanced_resume_text)
        encoded_pdf = base64.b64encode(enhanced_pdf).decode("utf-8")

        print("✅ Enhancement completed successfully.")
        return jsonify({
            "suggestions": suggestions,
            "enhanced_pdf": encoded_pdf
        })

    except Exception as e:
        print("❌ Enhancement Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
