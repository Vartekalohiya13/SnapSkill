
import streamlit as st
from io import BytesIO
from ats_checker2 import calculate_ats_score_with_job_pdf

st.title("📄 ATS Score – Compare Resume to Job Description")

resume_pdf = st.file_uploader("Upload your Resume (PDF)", type=["pdf"], key="resume")
job_pdf = st.file_uploader("Upload Job Description PDF", type=["pdf"], key="jd")

if st.button("Calculate ATS Score"):
    if resume_pdf and job_pdf:
        resume_bytes = BytesIO(resume_pdf.read())
        job_bytes = BytesIO(job_pdf.read())

        result = calculate_ats_score_with_job_pdf(resume_bytes, job_bytes)

        st.success(f"✅ ATS Score: {result['ats_score']}%")
        st.markdown(f"*Top Extracted Job Keywords:* {', '.join(result['job_keywords'])}")
        st.markdown(f"*Matched Keywords:* ✅ {', '.join(result['matched_keywords'])}")
        st.markdown(f"*Missing Keywords:* ❌ {', '.join(result['missing_keywords'])}")
        st.markdown("### 📝 Resume Preview (first 1000 characters):")
        st.text(result["resume_text_preview"])
        st.markdown("### 📄 Job Description Preview (first 1000 characters):")
        st.text(result["job_text_preview"])
    else:
        st.warning("Please upload both resume and job description PDFs.")