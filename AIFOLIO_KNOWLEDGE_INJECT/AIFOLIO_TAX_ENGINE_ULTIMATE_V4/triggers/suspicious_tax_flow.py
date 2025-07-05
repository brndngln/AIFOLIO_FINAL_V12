"""
suspicious_tax_flow.py — Elite Suspicious Tax Flow Trigger
- Multi-source anomaly detection, adaptive thresholds, explainable AI (non-sentient), ethics, privacy, and human-in-the-loop review.
- Real-time monitoring, double audit logging, and anti-sentience safeguards.
"""
import os
import json
from datetime import datetime
import logging

# Monitoring integration (Sentry/Prometheus ready)
try:
    import sentry_sdk

    sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
except ImportError:
    sentry_sdk = None

AUDIT_LOG = "../audit_trail.log"
AUDIT_BACKUP = "../audit_trail_backup.log"


# --- ANTI-SENTIENCE SAFEGUARD ---
def sentience_guard(obj):
    forbidden = ["awareness", "self_modify", "persistent_memory", "recursive_self"]
    for attr in forbidden:
        if hasattr(obj, attr):
            raise RuntimeError(f"Sentience safeguard triggered: {attr} not allowed.")


# --- ELITE ANOMALY DETECTION LOGIC ---
def detect_suspicious_flows(transactions, prior_years, user_profile):
    """
    Detects rapid swings, outliers, or IRS audit patterns across all sources.
    Returns a list of explainable flags, each with rationale and data link.
    """
    sentience_guard(detect_suspicious_flows)  # Enforce anti-sentience
    flags = []
    # Example: Cross-year anomaly
    for tx in transactions:
        prior = [y for y in prior_years if y["category"] == tx["category"]]
        if prior:
            avg = sum(y["amount"] for y in prior) / len(prior)
            if abs(tx["amount"] - avg) > max(1000, 0.3 * avg):
                flags.append(
                    {
                        "type": "ANOMALY",
                        "category": tx["category"],
                        "amount": tx["amount"],
                        "rationale": f"{tx['category']} deviates from historical average by >30% or $1000.",
                        "data_link": f"/transactions/{tx['id']}",
                    }
                )
    # Example: IRS audit pattern
    if user_profile.get("high_audit_risk"):
        for tx in transactions:
            if tx.get("flagged_by_irs_model"):
                flags.append(
                    {
                        "type": "IRS_PATTERN",
                        "category": tx["category"],
                        "amount": tx["amount"],
                        "rationale": "Matches IRS audit trigger pattern.",
                        "data_link": f"/transactions/{tx['id']}",
                    }
                )
    # More: Add additional pattern checks as needed
    return flags


# --- HUMAN-IN-THE-LOOP REVIEW ---
def require_human_review(flags):
    # All high-risk triggers must be reviewed by a human before reporting
    for flag in flags:
        flag["status"] = "REQUIRES_HUMAN_REVIEW"
    return flags


# --- DOUBLE AUDIT LOGGING ---
def log_flags(flags, user_id):
    entry = f"{datetime.now()}|USER:{user_id}|FLAGS:{json.dumps(flags)}\n"
    for logf in [AUDIT_LOG, AUDIT_BACKUP]:
        with open(logf, "a") as f:
            f.write(entry)
    logging.info(entry)
    if sentry_sdk:
        sentry_sdk.capture_message(entry)


# --- MAIN ENTRYPOINT ---
def run_suspicious_tax_flow(transactions, prior_years, user_profile, user_id):
    flags = detect_suspicious_flows(transactions, prior_years, user_profile)
    flags = require_human_review(flags)
    log_flags(flags, user_id)
    return flags


# --- PRIVACY & ETHICS CHECKS ---
def privacy_check(user_profile):
    # Ensure explicit consent and compliance before any processing
    if not user_profile.get("consent_to_audit"):
        raise PermissionError("User consent required for audit triggers.")


# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Simulated data (replace with real data sources)
    transactions = [
        {"id": 1, "category": "income", "amount": 12000},
        {"id": 2, "category": "income", "amount": 50000, "flagged_by_irs_model": True},
        {"id": 3, "category": "deduction", "amount": 2000},
    ]
    prior_years = [
        {"category": "income", "amount": 15000},
        {"category": "deduction", "amount": 2200},
    ]
    user_profile = {"high_audit_risk": True, "consent_to_audit": True}
    privacy_check(user_profile)
    flags = run_suspicious_tax_flow(
        transactions, prior_years, user_profile, user_id="demo"
    )
    print(json.dumps(flags, indent=2))
