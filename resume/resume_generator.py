from dotenv import load_dotenv
import os, asyncio
import cohere  # install with `pip install cohere`
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import convert_markdown_to_html, save_html_as_pdf , render_template_with_content , is_valid_template

load_dotenv()
cohere_key = os.getenv("COHERE_API_KEY")
if not cohere_key:
    raise ValueError("Missing COHERE_API_KEY")

# 1. Prompt setup
resume_prompt = PromptTemplate(
    input_variables=["experience"],
    template="""You are a resume expert... give clear and concise response including their hobbies too and don't ask user for any further changes or transformation in the provided output keep it accurate with thing that needs to be in a resume. we want resume in below format 
    1:Profile 
    2:Proffesional Snapshot
    3:Skills
    4:education Qualification
    5:Project Experience(minimum 3 project and their description with  user role should be added)
    6:Hobby
    7:Personal Details
    8:Disclaimer("generic disclaimer should be given to describe user profile and experience") 
    ### User Experience:\n{experience}\nReturn resume in Markdown."""
)

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
    if not is_valid_template(template):
        raise ValueError("Invalid template selected.")

    markdown = await generate_resume_markdown(experience)
    clean_md = clean_markdown(markdown)
    markdown_to_pdf(clean_md, output_path, template)
    return output_path  # Return file path for UI to serve/download


async def generate_resume_markdown(experience):
    return await get_chain().ainvoke({"experience": experience})

def markdown_to_pdf(md: str, path: str, template: str = "modern.html"):
    if not is_valid_template(template):
        raise ValueError("Invalid template selected.")
    
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

    markdown_to_pdf(clean_md, "test_resume.pdf", template=template)
    print("✅ Done!")


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
