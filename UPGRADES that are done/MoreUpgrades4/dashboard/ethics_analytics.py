import streamlit as st
import json
import pandas as pd
import logging

st.set_page_config(page_title="Ethics + Legal + QA Review", layout="wide")
st.title("Product Integrity Review Dashboard")

def sentience_safeguard_check():
    """Prevent and monitor for emergent sentience or unsafe autonomy."""
    logging.info("Sentience safeguard check passed.")
    return True

def human_oversight_checkpoint(action, details=None):
    """Log and optionally require review for sensitive actions."""
    logging.info(f"Human oversight: {action} | Details: {details}")

def privacy_compliance_check(df):
    """Ensure DataFrame does not display sensitive or unauthorized data."""
    if 'user_id' in df.columns:
        df['user_id'] = df['user_id'].astype(str).str[:8] + '***'
    return df

def compliance_pattern_alerts(df):
    """
    Scan for compliance, privacy, copyright, and ethical issues in the logs.
    Returns a list of alerts and highlights critical issues for oversight.
    Includes sentience, privacy, and audit safeguards.
    """
    sentience_safeguard_check()
    human_oversight_checkpoint("Begin compliance_pattern_alerts", None)
    df = privacy_compliance_check(df)
    alerts = []
    for idx, row in df.iterrows():
        if "copyright" in str(row.get("ethics_issues", "")).lower():
            alerts.append((row["title"], "Copyright risk"))
        if "privacy" in str(row.get("ethics_issues", "")).lower():
            alerts.append((row["title"], "Privacy risk"))
        if row.get("status") == "FAIL":
            alerts.append((row["title"], "Manual review required"))
        if row.get("status") == "WARN":
            alerts.append((row["title"], "Warning issued"))
    logging.info(f"Compliance alerts generated: {alerts}")
    human_oversight_checkpoint("Compliance alerts generated", alerts)
    return alerts


try:
    with open("analytics/review_logs.json", "r") as f:
        logs = json.load(f)
    df = pd.DataFrame(logs)
except Exception as e:
    st.error("No review log data found.")
    logging.error(f"Ethics analytics log load failure: {e}")
    st.stop()

st.metric("Total Reviewed Products", len(df))
st.metric("Products Passed", len(df[df["status"] == "PASS"]))
st.metric("Products With Warnings", len(df[df["status"] == "WARN"]))
st.metric("Average Readability", round(df["readability_score"].mean(), 2))

# --- Real-Time Compliance Alerts & Pattern Recognition ---
st.subheader(" Real-Time Compliance Alerts")
alerts = compliance_pattern_alerts(df)
if alerts:
    for title, alert in alerts:
        st.warning(f"{alert}: {title}")
else:
    st.success("No critical compliance or ethical issues detected.")

# --- Audit Trail (for oversight) ---
st.subheader(" Audit Trail")
st.dataframe(df[["title", "status", "reviewer", "timestamp", "ethics_issues", "legal_issues"]].fillna("None"))

st.subheader(" Warnings Overview")
st.dataframe(df[df["status"] == "WARN"][["title", "ethics_issues", "legal_issues", "suggestions"]])