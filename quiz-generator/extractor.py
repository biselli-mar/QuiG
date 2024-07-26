import re
import pymupdf
import pymupdf4llm
from pylatexenc.latex2text import LatexNodes2Text


# Text extraction functions
def extract_text_from_pdf(pdf_path):
    file = pymupdf.open(stream=pdf_path, filetype="pdf")  # sort=True
    md_text = pymupdf4llm.to_markdown(file, write_images=False, page_chunks=False)

    # remove multiple newlines and trailing whitespaces
    md_text = re.sub("\n\n+", "\n", md_text).strip()

    file.close()
    return md_text


def extract_text_from_latex(latex_path):
    with open(latex_path, 'r') as file:
        latex_content = file.read()
    text = LatexNodes2Text().latex_to_text(latex_content)
    return text
