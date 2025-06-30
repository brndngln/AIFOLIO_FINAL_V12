import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="🛡 Ethics + Legal + QA Review", layout="wide")
st.title("Product Integrity Review Dashboard")

try:
    with open("analytics/review_logs.json", "r") as f:
        logs = json.load(f)
    df = pd.DataFrame(logs)
except:
    st.error("No review log data found.")
    st.stop()

st.metric("Total Reviewed Products", len(df))
st.metric("Products Passed", len(df[df["status"] == "PASS"]))
st.metric("Products With Warnings", len(df[df["status"] == "WARN"]))
st.metric("Average Readability", round(df["readability_score"].mean(), 2))

st.subheader("🚨 Warnings Overview")
st.dataframe(df[df["status"] == "WARN"][["title", "ethics_issues", "legal_issues", "suggestions"]])