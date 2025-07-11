import os, asyncio
from dotenv import load_dotenv
import cohere

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .utils import (
    convert_markdown_to_html,
    save_html_as_pdf,
    render_template_with_content,
    is_valid_template,
)

# Load API key
load_dotenv()
cohere_key = os.getenv("COHERE_API_KEY")
if not cohere_key:
    raise ValueError("Missing COHERE_API_KEY")

# Prompt template
resume_prompt = PromptTemplate(
    input_variables=["experience"],
    template="""
You are a professional resume generator. Based on the user's experience, generate a clean, modern, and structured resume. This resume will be converted to HTML and then to PDF — so your output must use clean Markdown or HTML-compatible Markdown.

🧾 Strict Format Instructions:

📌 1. Date (Top-Right):
- Always Display today's date(the date on which the resume is made) in YYYY-MM-DD format.
- Align it to the top-right corner using: <div style='text-align:right; font-size:12px;'>YYYY-MM-DD</div>

📌 2. Font Styling:
- Use <h2>, <h3>, or <strong> for headings to show visual hierarchy.
- Ensure content uses <p style='font-size:13px;'>...</p> for readability.
- Avoid oversized fonts or headers.

📌 3. Section Order:
1. <h2>Profile</h2>
   - NAME and from the next line 2–3 lines about the candidate's strengths and experience.

2. <h2>Professional Snapshot</h2>
   - Use <ul> list for crisp points.

3. <h2 style='color:#007ACC;'>Skills</h2>
   - Format as HTML table with borders:
     <table style="border-collapse:collapse; width:100%;">
       <tr><th style="border:1px solid #ccc;">Skill</th><th style="border:1px solid #ccc;">Proficiency</th></tr>
       <tr><td style="border:1px solid #ccc;">Python</td><td style="border:1px solid #ccc;">Expert</td></tr>
     </table>

4. <h2>Education Qualification</h2>
   - Similar bordered HTML table with columns: Degree, Institution, Year.

5. <h2 style='color:#007ACC;'>Project Experience</h2>
   - At least 3 projects.
   - Use an HTML table with columns: Project Title, Role, Description.

6. <h2>Hobbies</h2>
   - Comma-separated list.

7.  <h2>Personal Details</h2>
   - Use HTML table:
     <table style="border-collapse:collapse; width:100%;">
       <tr><th style="border:1px solid #ccc;">Field</th><th style="border:1px solid #ccc;">Value</th></tr>
       <tr><td style="border:1px solid #ccc;">Name</td><td style="border:1px solid #ccc;">Vani Girdhar</td></tr>
       <tr><td style="border:1px solid #ccc;">LinkedIn</td><td style="border:1px solid #ccc;"><a href='https://www.linkedin.com/in/your-linkedin-username' target='_blank'>linkedin.com/in/your-linkedin-username</a></td></tr>
       <tr><td style="border:1px solid #ccc;">GitHub</td><td style="border:1px solid #ccc;"><a href='https://github.com/your-github-username' target='_blank'>github.com/your-github-username</a></td></tr>
     </table>

8. <h2>Disclaimer</h2>
     <p style='font-size:12px;'>(generic disclaimer should be given to describe user's profile and experience for professional purposes.)</p>

🚫 Don’ts:
- Do not write “Here is your resume” or any extra explanations or any question asking to improve the resume.
- Do not use Markdown code blocks (no 
).
- Ensure no content is outside the structure defined above.

Now generate the resume using this structure based on the user’s experience below:

Experience:
{experience}
"""
)



# LLM Wrapper
class CohereChatLLM:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
    async def __call__(self, prompt_value):
        resp = self.client.chat(
            model="command",
            message=prompt_value.text,
            temperature=0.7
        )
        return resp.text

# LangChain chain setup
def get_chain():
    return resume_prompt | CohereChatLLM(cohere_key) | StrOutputParser()

# Markdown cleaner
def clean_markdown(md: str) -> str:
    lines = md.splitlines()
    clean_lines = []
    for line in lines:
        if (
            "Here is your resume in Markdown" in line or
            "Let me know" in line or
            "Additional Information" in line or 
            "Would you like me to review" in line
        ):
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)

# Generate markdown from experience
async def generate_resume_markdown(experience: str):
    return await get_chain().ainvoke({"experience": experience})

# Full resume generation
async def generate_resume(experience: str, template: str = "modern.html", output_path: str = "resume.pdf"):
    print("⚙️ Template selected by user:", template)

    if not is_valid_template(template):
        raise ValueError("❌ Invalid template selected.")

    markdown = await generate_resume_markdown(experience)
    clean_md = clean_markdown(markdown)
    markdown_to_pdf(clean_md, output_path, template)
    return output_path

# Markdown → PDF
def markdown_to_pdf(md: str, path: str, template: str = "modern.html"):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # resume/
    templates_dir = os.path.join(base_dir, "templates")    # resume/templates
    template_path = os.path.join(templates_dir, template)

    if not os.path.isfile(template_path):
        raise ValueError(f"❌ Template not found at: {template_path}")

    html = convert_markdown_to_html(md)
    html = render_template_with_content(template, html)  # pass just the filename
    save_html_as_pdf(html, path)

# TEST FLOW
async def test_resume(template="professional.html"):
    sample = """-Name is Vani Girdhar
- Software Engineer at MICROSOFT (2021–2024): 
  - Led team of 5, improved system uptime by 20%
  - Created microservices in Python, deployed on AWS
  - Mentored junior devs and conducted code review.
  - Has won various Hackathons
- my github profile :- https://github.com/vanixyz
- my linkedin profile:- https://www.linkedin.com/in/vani-girdhar-0774aa322?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"""

    output_path = "test_resume.pdf"  # <-- you choose the path
    await generate_resume(sample, template=template, output_path=output_path)
    print(f"✅ PDF generated and saved to: {output_path}")


# Main
if __name__ == "__main__":
    asyncio.run(test_resume())
