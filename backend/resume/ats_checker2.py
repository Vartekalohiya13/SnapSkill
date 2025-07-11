
# import re
# import PyPDF2
# from typing import List, Dict
# from io import BytesIO

# def extract_text_from_pdf(pdf_file: BytesIO) -> str:
#     """Extracts text content from a PDF file."""
#     reader = PyPDF2.PdfReader(pdf_file)
#     full_text = ""
#     for page in reader.pages:
#         full_text += page.extract_text() or ""
#     return full_text

# def preprocess_text(text: str) -> str:
#     """Cleans and lowers the text for matching."""
#     return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()

# def extract_keywords_from_job_description(job_text: str, top_n: int = 20) -> List[str]:
#     """Extracts the most frequent non-trivial words from the job description."""
#     stopwords = set([
#         'and', 'or', 'with', 'for', 'to', 'in', 'of', 'on', 'a', 'an', 'the', 'is', 'are',
#         'we', 'you', 'will', 'this', 'your', 'as', 'be', 'that', 'our', 'by', 'at'
#     ])
    
#     words = preprocess_text(job_text).split()
#     filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    
#     freq = {}
#     for word in filtered_words:
#         freq[word] = freq.get(word, 0) + 1
    
#     sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
#     top_keywords = [word for word, count in sorted_words[:top_n]]
    
#     return top_keywords

# def calculate_ats_score_with_job_pdf(resume_pdf: BytesIO, job_pdf: BytesIO) -> Dict[str, any]:
#     """
#     Reads both resume and job PDFs and calculates ATS score.

#     Args:
#         resume_pdf (BytesIO): The uploaded resume PDF.
#         job_pdf (BytesIO): The uploaded job description PDF.

#     Returns:
#         Dict[str, any]: ATS score report with matched/missing keywords.
#     """
#     resume_text = extract_text_from_pdf(resume_pdf)
#     job_text = extract_text_from_pdf(job_pdf)
    
#     keywords = extract_keywords_from_job_description(job_text)
#     resume_processed = preprocess_text(resume_text)

#     matched_keywords = []
#     missing_keywords = []

#     for keyword in keywords:
#         if re.search(rf'\b{re.escape(keyword)}\b', resume_processed):
#             matched_keywords.append(keyword)
#         else:
#             missing_keywords.append(keyword)

#     score = round((len(matched_keywords) / len(keywords)) * 100, 2) if keywords else 0

#     return {
#         "ats_score": score,
#         "matched_keywords": matched_keywords,
#         "missing_keywords": missing_keywords,
#         "total_keywords": len(keywords),
#         "resume_text_preview": resume_text[:1000],
#         "job_text_preview": job_text[:1000],
#         "job_keywords": keywords
#     }