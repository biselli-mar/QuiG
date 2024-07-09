import PyPDF2
import pymupdf
import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter
from pylatexenc.latex2text import LatexNodes2Text
from langchain_community.document_loaders import PyMuPDFLoader


# Text extraction functions
def extract_text_from_pdf(pdf_path):
    file = pymupdf.open(stream=pdf_path, filetype="pdf")
    md_text = pymupdf4llm.to_markdown(file, write_images=False, page_chunks=False)
    # splitter = MarkdownTextSplitter(chunk_size=40, chunk_overlap=10)
    # docs = splitter.create_documents([md_text])
    # text = ""
    # for doc in md_text:  # only necessary because of page_chunks=True
    #    text += doc
    file.close()
    return md_text


def extract_text_from_latex(latex_path):
    with open(latex_path, 'r') as file:
        latex_content = file.read()
    text = LatexNodes2Text().latex_to_text(latex_content)
    return text
