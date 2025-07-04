# utils.py

import markdown
import pdfkit
import os


config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML."""
    return markdown.markdown(markdown_text)

def save_html_as_pdf(html_content: str, output_path: str) -> None:
    """Save HTML as PDF using pdfkit."""
    # Ensure wkhtmltopdf is installed and configured correctly
    options = {
        'enable-local-file-access': None
    }
    pdfkit.from_string(html_content, output_path, options=options)


