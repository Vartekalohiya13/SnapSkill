import os
import markdown
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os 
env = Environment(loader=FileSystemLoader("templates"))


def convert_markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text)

def render_template_with_content(template_path: str, resume_content: str) -> str:
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("{{ content }}", resume_content)

def save_html_as_pdf(html_content: str, output_path: str) -> None:
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Users\hpnar\OneDrive\Desktop\ai resume builder\SnapSkill-1\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    options = {
        "enable-local-file-access": None
    }
    pdfkit.from_string(html_content, output_path, options=options, configuration=config)





def is_valid_template(template_name: str) -> bool:
    path = os.path.join("templates", template_name)
    return os.path.isfile(path)


