# test_pdfkit.py
from utils import save_html_as_pdf

html = """
<h1>Test Resume</h1>
<ul>
    <li>Python Developer</li>
    <li>FastAPI Specialist</li>
</ul>
"""

save_html_as_pdf(html, "test_output.pdf")
print("PDF generated successfully! Check test_output.pdf")