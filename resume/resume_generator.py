from dotenv import load_dotenv
import os, asyncio
import cohere  # install with `pip install cohere`
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import convert_markdown_to_html, save_html_as_pdf

load_dotenv()
cohere_key = os.getenv("COHERE_API_KEY")
if not cohere_key:
    raise ValueError("Missing COHERE_API_KEY")

# 1. Prompt setup
resume_prompt = PromptTemplate(
    input_variables=["experience"],
    template="""You are a resume expert...### User Experience:\n{experience}\nReturn resume in Markdown."""
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

async def generate_resume_markdown(experience):
    return await get_chain().ainvoke({"experience": experience})

def markdown_to_pdf(m, path):
    html = convert_markdown_to_html(m)
    save_html_as_pdf(html, path)


#test flow
async def test_resume():
    sample ="""- Software Engineer at XYZ Corp (2021–2024): 
  - Led team of 5, improved system uptime by 20%
  - Created microservices in Python, deployed on AWS
  - Mentored junior devs and conducted code review."""
    md = await generate_resume_markdown(sample)
    print(md)
    markdown_to_pdf(md, "test_resume.pdf")
    print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(test_resume())
