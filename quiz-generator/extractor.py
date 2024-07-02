import PyPDF2
from pylatexenc.latex2text import LatexNodes2Text


# Text extraction functions
def extract_text_from_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


def extract_text_from_latex(latex_path):
    with open(latex_path, 'r') as file:
        latex_content = file.read()
    text = LatexNodes2Text().latex_to_text(latex_content)
    return text
