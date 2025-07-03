import streamlit as st
import json
# Emma Compliance Lock
OWNER_LOCK = True
import os
import time

EVENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_event_log.jsonl'))

st.set_page_config(page_title="Vault Dashboard (Realtime)", layout="wide")
st.title("Vault Dashboard (Realtime)")

last_len = 0
placeholder = st.empty()

while True:
    with open(EVENT_LOG) as f:
        lines = f.readlines()
    if len(lines) != last_len:
        last_len = len(lines)
        events = [json.loads(line) for line in lines[-50:]]
        with placeholder.container():
            st.write("### Recent Vault Events")
            for e in reversed(events):
                st.json(e)
    time.sleep(2)
