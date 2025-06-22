import streamlit as st
import json
import os

EVENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_event_log.jsonl'))

st.set_page_config(page_title="Vault Event Viewer", layout="wide")
st.title("Vault Event Viewer")

with open(EVENT_LOG) as f:
    lines = f.readlines()

st.write("### Recent Vault Events")
for line in reversed(lines[-100:]):
    event = json.loads(line)
    st.json(event)
