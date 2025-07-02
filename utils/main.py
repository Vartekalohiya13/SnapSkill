#fast api server 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from resume_generator import generate_resume_markdown, markdown_to_pdf
import uuid

app = FastAPI()

# Allow CORS (React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify React domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    experience: str

@app.post("/generate-resume")
async def generate_resume(data: ResumeRequest):
    markdown = await generate_resume_markdown(data.experience)
    
    filename = f"resume_{uuid.uuid4().hex[:8]}.pdf"
    pdf_path = f"resumes/{filename}"
    
    markdown_to_pdf(markdown, pdf_path)

    return {
        "markdown": markdown,
        "pdf_url": f"/resumes/{filename}"
    }
