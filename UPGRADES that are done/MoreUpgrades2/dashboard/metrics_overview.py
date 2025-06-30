import streamlit as st
from analytics.funnel_metrics import get_funnel_metrics

st.set_page_config(page_title="📈 AIFOLIO Funnel Metrics", layout="centered")

st.title("Funnel Performance Overview")

metrics = get_funnel_metrics()
if not metrics:
    st.warning("No funnel data available.")
else:
    st.metric("Total Downloads", metrics["downloads"])
    st.metric("Total Purchases", metrics["purchases"])
    st.metric("Upsells", metrics["upsells"])
    st.metric("Conversion Rate", f"{metrics['conversion_rate']}%")

    st.subheader("Top Products")
    for product, stats in metrics["top_products"].items():
        st.markdown(f"**{product}** — Downloads: {stats['downloads']}, Purchases: {stats['purchases']}, Upsells: {stats['upsells']}")

    st.subheader("Drop-Off Points")
    for product, count in metrics["drop_off_points"].items():
        st.markdown(f"- {product}: {count} drop-offs")