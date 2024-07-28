import re
import pymupdf
import pymupdf4llm
from pylatexenc.latex2text import LatexNodes2Text


def extract_text_from_pdf(pdf_stream):
    file = pymupdf.open(stream=pdf_stream, filetype="pdf")  # sort=True
    md_text = pymupdf4llm.to_markdown(file, write_images=False, page_chunks=False)
    md_text = clean_text(md_text)

    file.close()
    return md_text


def extract_text_from_latex(latex_stream):
    latex_content = latex_stream.decode("utf-8")
    text = LatexNodes2Text().latex_to_text(latex_content)
    text = clean_text(text)

    return text


def clean_text(text):
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n\s*\n+', '\n', text)

    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple tabs with a single tab
    text = re.sub(r'\t+', '\t', text)

    # Ensure lines containing only tabs or spaces are reduced to a single newline
    lines = text.split('\n')
    lines = [line if not re.match(r'^\s*$', line) else '' for line in lines]
    text = '\n'.join(lines)

    # Strip leading and trailing whitespace from the entire text
    text = text.strip()

    return text
