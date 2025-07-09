#utilis.py
import markdown
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os 
env = Environment(loader=FileSystemLoader("templates"))


def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML."""
    return markdown.markdown(markdown_text)

def render_template_with_content(template_name: str, html_content: str) -> str:
    """Render the selected Jinja2 template with the given HTML content."""
    template = env.get_template(template_name)
    return template.render(content=html_content)

def save_html_as_pdf(html_content: str, output_path: str) -> None:
    """Save HTML as PDF using pdfkit with correct wkhtmltopdf configuration."""
    # 🔧 Tell pdfkit exactly where wkhtmltopdf.exe lives
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Users\hpnar\OneDrive\Desktop\ai resume builder\SnapSkill-1\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Adjust this path as needed
    )
    options = {
        "enable-local-file-access": None
    }
    # ⚠️ Pass the configuration here
    pdfkit.from_string(html_content, output_path, options=options, configuration=config)

def is_valid_template(template_name: str) -> bool:
    path = os.path.join("templates", template_name)
    return os.path.isfile(path)


