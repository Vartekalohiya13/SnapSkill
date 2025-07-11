from flask import Flask, request, make_response, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import fitz  # PyMuPDF
import markdown
import pdfkit
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import io

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your OpenAI key
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
You are an AI resume expert. Below is the raw text extracted from a candidate's resume.

Your tasks:
1. Provide actionable AI suggestions to improve the resume for ATS (aim for a 90+ score).
2. If important sections like 'Projects', 'Links', or 'Summary' are missing, suggest them.
3. Output suggestions first.
4. Then, rewrite the resume in polished markdown (no bullet points).

Resume:
{text}
"""
)

def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "".join(page.get_text() for page in doc)

def markdown_to_pdf(md_content, output_path):
    html = markdown.markdown(md_content)
    pdfkit.from_string(html, output_path)

@app.route("/enhance", methods=["POST"])
def enhance_resume():
    uploaded_file = request.files.get("resume")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded."}), 400

    print("✅ File received:", uploaded_file.filename)

    try:
        resume_text = extract_text_from_pdf(uploaded_file)
        print("📄 Extracted resume text:", resume_text[:500])
    except Exception as e:
        print("❌ Error reading PDF:", str(e))
        return jsonify({"error": "Failed to extract text from resume."}), 500

    try:
        chain = LLMChain(llm=llm, prompt=prompt_template)
        result = chain.run(resume_text)
        print("🧠 LLM Output:", result[:500])
    except Exception as e:
        print("❌ LLM error:", str(e))
        return jsonify({"error": "AI processing failed."}), 500

    # Split suggestions and markdown
    if "##" in result:
        parts = result.split("##", 1)
        suggestions = parts[0].strip()
        markdown_resume = "##" + parts[1].strip()
    else:
        suggestions = "No suggestions found."
        markdown_resume = result.strip()

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            markdown_to_pdf(markdown_resume, tmp_file.name)
            pdf_data = open(tmp_file.name, "rb").read()
            os.unlink(tmp_file.name)
    except Exception as e:
        print("❌ PDF generation failed:", str(e))
        return jsonify({"error": "Failed to generate PDF."}), 500

    response = make_response(pdf_data)
    response.headers.set("Content-Type", "application/pdf")
    response.headers.set("Content-Disposition", "attachment", filename="enhanced_resume.pdf")
    response.headers.set("X-Suggestions", suggestions)
    return response

@app.route("/test-pdf", methods=["GET"])
def test_pdf():
    html = "<h1>Hello from SnapSkill</h1><p>This is a test PDF.</p>"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdfkit.from_string(html, temp_pdf.name)
        pdf_bytes = open(temp_pdf.name, "rb").read()
        os.unlink(temp_pdf.name)
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
