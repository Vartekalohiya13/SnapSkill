from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from utils import convert_markdown_to_html, save_html_as_pdf
import os 

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
print("API KEY:", os.getenv("OPENAI_API_KEY"))


resume_prompt = PromptTemplate(
        input_variables=["experience"],
        template="""
You are an expert resume writer with deep knowledge of modern hiring practices.

Using the information provided below, generate a professional, ATS-optimized resume in clean markdown format. Structure it into the following sections:
- **Professional Summary** (2 to 3 concise, compelling sentences)
- **Core Skills** (bulleted list of 8 to 12 skills relevant to the experience)
- **Professional Experience** (reverse-chronological bullet points with clear impact and quantifiable achievements)
- **Education** (include degree, institution, and dates if available)

Ensure:
- Use of strong action verbs
- Quantified accomplishments where possible (e.g. “Increased sales by 20%”)
- Clear formatting (no tables)

### User Experience:
{experience}

Return the resume only in valid markdown format.
"""
 )

def get_llm():
    if not openai_api_key:
        raise ValueError("Missing OpenAI API key in environment variables.")
    return ChatOpenAI(
    temperature=0.7,
      model_name="gpt-3.5-turbo",
     openai_api_key=openai_api_key
    )
async def generate_resume_markdown(experience: str) -> str:
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=resume_prompt)
    result = await chain.ainvoke({"experience": experience})
    return result["text"]

def markdown_to_pdf(markdown: str, pdf_path: str):
    html = convert_markdown_to_html(markdown)
    save_html_as_pdf(html, pdf_path)

