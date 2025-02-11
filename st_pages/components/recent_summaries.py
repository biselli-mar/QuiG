import streamlit as st
import json
import datetime

from const import RECENT_SUMMARIES_PATH

selected_summaries = []

@st.dialog("Save Summary")
def append_summary_dialog():
    f_recent_summaries = open(RECENT_SUMMARIES_PATH, "r")
    recent_summaries = f_recent_summaries.read()
    if recent_summaries == "":
        recent_summaries = "[]"
    f_recent_summaries.close()
    time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    summary = st.session_state.last_summary
    with st.form(key="append_summary"):
        title = st.text_input("Title", value="Recent Summary", placeholder="Enter a title for the summary.")
        summary_input = st.text_area("Text", summary, height=200)
        col1, col2 = st.columns([1, 1])
        with col1:
            save = st.form_submit_button("Save", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        if save:
            summaries_json = json.loads(recent_summaries)
            summaries_json.append({"time":f"{time_now}","title":f"{title}","summary":summary_input})
            append_summary(summaries_json)
            st.rerun()
            st.write("Summary saved.")
        if cancel:
            st.rerun()

def append_summary(recent_summaries):
    f_recent_summaries = open(RECENT_SUMMARIES_PATH, "w")
    f_recent_summaries.write(json.dumps(recent_summaries, default=lambda x: x.__dict__))
    f_recent_summaries.close()

def recent_summary_selector(summaries_json):
    with st.container(key="summary_selector", height=520, border=False):
        for i, summary in enumerate(summaries_json):
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("Select",
                                       key=f"select_summary_{i}",
                                       label_visibility="collapsed")
                
            with col2:
                st.text_area(f"{summary['title']} {summary['time']}", summary['summary'], height=200, disabled=True)

            if selected:
                selected_summaries.append(summary['summary'])
    if st.button("Generate from selected summaries"):
        return selected_summaries
    return None