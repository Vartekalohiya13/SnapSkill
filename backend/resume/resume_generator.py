from dotenv import load_dotenv
import os, asyncio
import cohere  # install with `pip install cohere`
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .utils import (
    convert_markdown_to_html,
    save_html_as_pdf,
    render_template_with_content,
    is_valid_template,
)

load_dotenv()
cohere_key = os.getenv("COHERE_API_KEY")
if not cohere_key:
    raise ValueError("Missing COHERE_API_KEY")

# 1. Prompt setup

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

7. <h2>Personal Details</h2>
   - Use HTML table:
     <table style="border-collapse:collapse; width:100%;">
       <tr><th style="border:1px solid #ccc;">Field</th><th style="border:1px solid #ccc;">Value</th></tr>
       <tr><td style="border:1px solid #ccc;">Name</td><td style="border:1px solid #ccc;">Vani Girdhar</td></tr>
     </table>

8. <h2>Disclaimer</h2>
     <p style='font-size:12px;'>(generic disclaimer should be given to describe user's profile and experience for professional purposes.)</p>

🚫 Don’ts:
- Do not write “Here is your resume” or any extra explanations or any question asking to improve the resume.
- Do not use Markdown code blocks (no ```).
- Ensure no content is outside the structure defined above.

Now generate the resume using this structure based on the user’s experience below:

Experience:
{experience}
"""
)


# resume_prompt = PromptTemplate(
#     input_variables=["experience"],
#     template="""You are a resume expert... give clear and concise response including their hobbies too and don't ask user for any further changes or transformation in the provided output keep it accurate with thing that needs to be in a resume. we want resume in below format 
#     1:Profile 
#     2:Proffesional Snapshot
#     3:Skills
#     4:education Qualification
#     5:Project Experience(minimum 3 project and their description with  user role should be added)
#     6:Hobby
#     7:Personal Details
#     8:Disclaimer("generic disclaimer should be given to describe user profile and experience") 
#     ### User Experience:\n{experience}\nReturn resume in Markdown."""
# )

# 2. Cohere chat wrapper for LCEL
class CohereChatLLM:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
    async def __call__(self, prompt_value):
        resp = self.client.chat(
            model="command",  # trial tier model
            message=prompt_value.text,
            temperature=0.7
        )
        return resp.text

# 3. Build pipeline: prompt → cohere LLM → parser
def get_chain():
    return resume_prompt | CohereChatLLM(cohere_key) | StrOutputParser()

async def generate_resume(experience: str, template: str = "modern.html", output_path: str = "resume.pdf"):
  # ✅ Get absolute path to template
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.abspath(os.path.join(base_dir, "..", "templates", template))

    print(f"🧠 Checking path: {template_path}")
    if not os.path.isfile(template_path):
        raise ValueError(f"❌ Invalid template selected: {template}")

    markdown = await generate_resume_markdown(experience)
    clean_md = clean_markdown(markdown)
    markdown_to_pdf(clean_md, output_path, template)
    return output_path  # Return file path for UI to serve/download

async def generate_resume_markdown(experience: str):
    return await get_chain().ainvoke({"experience": experience})

async def generate_resume(experience: str, template: str = "modern.html", output_path: str = "resume.pdf"):
    from .utils import is_valid_template  # make sure it's imported

    print("⚙️ Template selected by user:", template)

    if not is_valid_template(template):
        raise ValueError("❌ Invalid template selected.")

    markdown = await generate_resume_markdown(experience)
    clean_md = clean_markdown(markdown)
    markdown_to_pdf(clean_md, output_path, template)
    return output_path

def markdown_to_pdf(md: str, path: str, template_path: str):
    if not is_valid_template(template):
        raise ValueError(f"❌ Template not found: {template}")

    html = convert_markdown_to_html(md)
    html = render_template_with_content(template, html)
    save_html_as_pdf(html, path)

#test flow
async def test_resume(template="professional.html"):
    sample ="""-Name is Vani Girdhar
    - Software Engineer at MICROSOFT (2021–2024): 
  - Led team of 5, improved system uptime by 20%
  - Created microservices in Python, deployed on AWS
  - Mentored junior devs and conducted code review.
  - Has won various Hackathons"""
    
    md = await generate_resume_markdown(sample)
    clean_md = clean_markdown(md)
    print(clean_md)

def markdown_to_pdf(md: str, path: str, template: str = "modern.html"):
    from .utils import convert_markdown_to_html, render_template_with_content, save_html_as_pdf, is_valid_template

    # Get absolute path to backend/templates/template.html
    base_dir = os.path.dirname(os.path.abspath(__file__))  # resume/
    templates_dir = os.path.join(base_dir, "..", "templates")  # backend/templates
    full_template_path = os.path.abspath(os.path.join(templates_dir, template))

    if not os.path.isfile(full_template_path):
        raise ValueError(f"❌ Template not found at: {full_template_path}")

    html = convert_markdown_to_html(md)
    html = render_template_with_content(full_template_path, html)
    save_html_as_pdf(html, path)


def clean_markdown(md: str) -> str:
    """Remove any boilerplate or markdown sections that don't belong in the resume."""
    lines = md.splitlines()
    clean_lines = []
    for line in lines:
        if (
            "Here is your resume in Markdown" in line or
            "Let me know" in line or
            "Additional Information" in line or 
            "Would you like me to review this resume and make any other changes that may be necessary?" in line
        ):
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)


if __name__ == "__main__":
    asyncio.run(test_resume())
