import json
import os
import streamlit as st
import glob

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../analytics/"))

st.set_page_config(page_title="AI Output Transparency Explorer", layout="wide")
st.title("AI Output Transparency Explorer")

log_files = glob.glob(os.path.join(LOG_DIR, "*log.jsonl"))
selected_log = st.selectbox("Select a log file to explore:", log_files)

if selected_log:
    st.write(f"### Viewing: {os.path.basename(selected_log)}")
    with open(selected_log) as f:
        lines = f.readlines()
    if not lines:
        st.info("No entries found.")
    else:
        for i, line in enumerate(reversed(lines[-200:])):
            try:
                entry = json.loads(line)
                with st.expander(f"Entry {len(lines)-i}"):
                    st.json(entry)
            except Exception as e:
                st.warning(f"Malformed line: {e}")
