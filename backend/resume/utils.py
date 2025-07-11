import os
import markdown
import pdfkit
from jinja2 import Environment, FileSystemLoader

# 👇 This makes the path absolute, relative to this utils.py file
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def convert_markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text)

def render_template_with_content(template_name: str, html_content: str) -> str:
    template = env.get_template(template_name)
    return template.render(content=html_content)

def save_html_as_pdf(html_content: str, output_path: str) -> None:
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Users\hpnar\OneDrive\Desktop\ai resume builder\SnapSkill-1\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    options = {
        "enable-local-file-access": None
    }
    pdfkit.from_string(html_content, output_path, options=options, configuration=config)

def is_valid_template(template_name: str) -> bool:
    path = os.path.join(TEMPLATE_DIR, template_name)
    return os.path.isfile(path)
