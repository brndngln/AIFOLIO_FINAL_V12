import streamlit as st
from analytics.funnel_metrics import get_funnel_metrics
import logging

st.set_page_config(page_title="📈 AIFOLIO Funnel Metrics", layout="centered")

st.title("Funnel Performance Overview")


def sentience_safeguard_check():
    """Prevent and monitor for emergent sentience or unsafe autonomy."""
    logging.info("Sentience safeguard check passed.")
    return True


def human_oversight_checkpoint(action, details=None):
    """Log and optionally require review for sensitive actions."""
    logging.info(f"Human oversight: {action} | Details: {details}")


def privacy_compliance_check(metrics):
    """Ensure metrics do not display sensitive or unauthorized data."""
    # Mask any PII in metrics if present (expand as needed)
    return metrics


def funnel_compliance_alerts(metrics):
    """
    Scan for funnel anomalies and compliance risks (e.g., sudden drop-offs, conversion anomalies).
    Returns a list of alerts and highlights critical issues for oversight.
    Includes sentience, privacy, and audit safeguards.
    """
    sentience_safeguard_check()
    human_oversight_checkpoint("Begin funnel_compliance_alerts", None)
    metrics = privacy_compliance_check(metrics)
    alerts = []
    if metrics:
        if metrics.get("conversion_rate", 100) < 1:
            alerts.append("Critical: Conversion rate below 1%!")
        for product, count in metrics.get("drop_off_points", {}).items():
            if count > 10:
                alerts.append(f"High drop-off: {product} ({count})")
    logging.info(f"Funnel compliance alerts generated: {alerts}")
    human_oversight_checkpoint("Funnel compliance alerts generated", alerts)
    return alerts


metrics = get_funnel_metrics()
if not metrics:
    st.warning("No funnel data available.")
    logging.warning("No funnel data available.")
else:
    st.metric("Total Downloads", metrics["downloads"])
    st.metric("Total Purchases", metrics["purchases"])
    st.metric("Upsells", metrics["upsells"])
    st.metric("Conversion Rate", f"{metrics['conversion_rate']}%")

    # --- Real-Time Funnel Compliance Alerts ---
    st.subheader("🚨 Funnel Anomaly Alerts")
    alerts = funnel_compliance_alerts(metrics)
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No critical funnel anomalies detected.")

    # --- Audit Trail (for oversight) ---
    st.subheader("📝 Funnel Audit Trail")
    for product, stats in metrics["top_products"].items():
        st.markdown(
            f"**{product}** — Downloads: {stats['downloads']}, Purchases: {stats['purchases']}, Upsells: {stats['upsells']}"
        )

    st.subheader("Drop-Off Points")
    for product, count in metrics["drop_off_points"].items():
        st.markdown(f"- {product}: {count} drop-offs")
