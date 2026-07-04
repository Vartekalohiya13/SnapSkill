# SnapSkill – AI-Powered Resume Builder

An AI-powered full-stack resume builder that generates 
professional resumes in minutes.

## Tech Stack
- **Backend** – Flask, LangChain, Cohere LLM
- **Frontend** – React.js, Streamlit
- **PDF Generation** – Jinja2 templates + wkhtmltopdf
- **API** – REST APIs connecting frontend to backend

## Features
- AI-generated resume content based on user input
- Multiple resume templates
- One-click PDF download
- 70% reduction in output errors via prompt optimization
- Reduces resume creation time by 12 minutes per user

## Architecture
User Input → React Frontend → Flask REST API 
→ LangChain + Cohere LLM → Jinja2 Template 
→ wkhtmltopdf → PDF Output

## How to Run
### Backend
cd backend
pip install -r requirements.txt
python app.py

### Frontend
cd frontend
npm install
npm start


