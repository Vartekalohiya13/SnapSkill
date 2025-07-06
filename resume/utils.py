#utilis.py
import markdown
import pdfkit

def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML."""
    return markdown.markdown(markdown_text)

def save_html_as_pdf(html_content: str, output_path: str) -> None:
    """Save HTML as PDF using pdfkit with correct wkhtmltopdf configuration."""
    # 🔧 Tell pdfkit exactly where wkhtmltopdf.exe lives
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Users\hpnar\OneDrive\Desktop\ai resume builder\SnapSkill-1\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    options = {
        "enable-local-file-access": None
    }
    # ⚠️ Pass the configuration here
    pdfkit.from_string(html_content, output_path, options=options, configuration=config)

