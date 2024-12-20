import logging
import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import MarkdownTextSplitter

from const import MAX_TOKENS, CHUNK_SIZE, CHUNK_OVERLAP
from generation.llm import llm


def summarize_docs(docs, summary_content=None):
    """
    Summarize the list of document chunks using a map-reduce chain.

    Args:
        docs (list): The list of document chunks to be summarized.

    Returns:
        str: The summarized text.
    """

    map_prompt = PromptTemplate(template=st.session_state.map_prompt, input_variables=["text"])
    reduce_prompt = PromptTemplate(template=st.session_state.reduce_prompt, input_variables=["text"])
    
    if summary_content is not None:
        map_prompt = PromptTemplate(template=st.session_state.map_prompt_limited, input_variables=["text", "summary_content"])
        reduce_prompt = PromptTemplate(template=st.session_state.reduce_prompt_limited, input_variables=["text", "summary_content"])
    sum_chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=reduce_prompt,
        token_max=MAX_TOKENS
    )

    logging.info("Invoking map-reduce chain...")
    summary = sum_chain.invoke({"input_documents":docs,"summary_content":summary_content})
    logging.info("Map-reduce chain finished.")

    logging.info("Summary: %s", summary["output_text"])
    return summary["output_text"]


@st.cache_data(ttl=3600, show_spinner=False)
def split_text(text):
    """
    Split the input text into smaller chunks using MarkdownTextSplitter.

    Args:
        text (str): The input text to be split.

    Returns:
        list: A list of document chunks.
    """
    logging.info("Text length: %s", len(text))
    splitter = MarkdownTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP)
    doc_list = splitter.create_documents([text])
    logging.info("Text split into %s document(s).", len(doc_list))
    return doc_list
