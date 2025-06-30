import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AIFOLIO™ Performance Dashboard", layout="wide")

try:
    with open("analytics/review_logs.json", "r") as f:
        logs = json.load(f)
    df = pd.DataFrame(logs)
except Exception as e:
    st.error(f"Error loading logs: {e}")
    st.stop()

st.title("📊 AIFOLIO™ Performance & Compliance Dashboard")
st.markdown("### Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df))
col2.metric("Avg. Readability Score", round(df["readability_score"].mean(), 2))
col3.metric("Manual Reviews Needed", len(df[df["status"] == "FAIL"]))

st.subheader("⚠️ Ethics / Legal Issue Reports")
st.dataframe(df[["title", "ethics_issues", "legal_issues", "status"]].fillna("None"))

st.subheader("💡 Optimization Suggestions")
for _, row in df.iterrows():
    if row["status"] == "WARN":
        st.markdown(f"- **{row['title']}**: {row['suggestions']}")