import re
import pymupdf
import pymupdf4llm
from pylatexenc.latex2text import LatexNodes2Text
import streamlit as st


@st.cache_data(ttl=3600, show_spinner=False)
def extract_text(file):
    if file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(file.read())
    else:
        extracted_text = extract_text_from_latex(file.read())

    return extracted_text


def extract_text_from_pdf(pdf_stream):
    file = pymupdf.open(stream=pdf_stream, filetype="pdf")
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
    # Replace multiple newlines, spaces and tabs with single ones
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\t+", "\t", text)

    # Ensure lines containing only tabs or spaces are reduced to a single newline
    lines = text.split("\n")
    lines = [line if not re.match(r"^\s*$", line) else "" for line in lines]
    text = "\n".join(lines).strip()

    return text
