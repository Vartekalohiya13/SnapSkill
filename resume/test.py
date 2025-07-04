import asyncio
from resume_generator import generate_resume_markdown, markdown_to_pdf

async def test_resume_flow():
    experience = """
    Software Engineer at ABC Corp (2020-2023):
    - Developed a Python-based resume generator
    - Increased system efficiency by 30%
    Education: B.Tech in Computer Science
    """
    
    print("Generating markdown...")
    try:
        markdown = await generate_resume_markdown(experience)
        print("\nGenerated Markdown:\n", markdown)
        
        print("\nExporting to PDF...")
        pdf_path = "test_resume.pdf"
        markdown_to_pdf(markdown, pdf_path)
        print(f"PDF saved to: {pdf_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_resume_flow())