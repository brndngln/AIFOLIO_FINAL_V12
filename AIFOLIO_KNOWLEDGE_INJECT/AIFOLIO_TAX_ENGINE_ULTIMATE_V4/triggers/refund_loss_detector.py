"""
refund_loss_detector.py — Elite Refund Loss Detector
- Deduction trend analysis, explainable AI (non-sentient), ethics, privacy, and human-in-the-loop review.
- Real-time monitoring, double audit logging, and anti-sentience safeguards.
"""
import os
import json
from datetime import datetime
import logging

try:
    import sentry_sdk

    sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
except ImportError:
    sentry_sdk = None

AUDIT_LOG = "../audit_trail.log"
AUDIT_BACKUP = "../audit_trail_backup.log"


def sentience_guard(obj):
    forbidden = ["awareness", "self_modify", "persistent_memory", "recursive_self"]
    for attr in forbidden:
        if hasattr(obj, attr):
            raise RuntimeError(f"Sentience safeguard triggered: {attr} not allowed.")


def detect_refund_loss(deductions, prior_years, user_profile):
    """
    Detects missing or declining deductions before tax season.
    Returns a list of explainable flags, each with rationale and data link.
    """
    sentience_guard(detect_refund_loss)
    flags = []
    for d in deductions:
        prior = [y for y in prior_years if y["category"] == d["category"]]
        if prior:
            avg = sum(y["amount"] for y in prior) / len(prior)
            if d["amount"] < 0.7 * avg:
                flags.append(
                    {
                        "type": "DEDUCTION_DROP",
                        "category": d["category"],
                        "amount": d["amount"],
                        "rationale": f"Deduction for {d['category']} fell below 70% of historical average.",
                        "data_link": f"/deductions/{d['id']}",
                    }
                )
    return flags


def require_human_review(flags):
    for flag in flags:
        flag["status"] = "REQUIRES_HUMAN_REVIEW"
    return flags


def log_flags(flags, user_id):
    entry = f"{datetime.now()}|USER:{user_id}|REFUND_FLAGS:{json.dumps(flags)}\n"
    for logf in [AUDIT_LOG, AUDIT_BACKUP]:
        with open(logf, "a") as f:
            f.write(entry)
    logging.info(entry)
    if sentry_sdk:
        sentry_sdk.capture_message(entry)


def run_refund_loss_detector(deductions, prior_years, user_profile, user_id):
    flags = detect_refund_loss(deductions, prior_years, user_profile)
    flags = require_human_review(flags)
    log_flags(flags, user_id)
    return flags


def privacy_check(user_profile):
    if not user_profile.get("consent_to_audit"):
        raise PermissionError("User consent required for deduction triggers.")


if __name__ == "__main__":
    deductions = [
        {"id": 1, "category": "home_office", "amount": 500},
        {"id": 2, "category": "supplies", "amount": 100},
    ]
    prior_years = [
        {"category": "home_office", "amount": 900},
        {"category": "supplies", "amount": 300},
    ]
    user_profile = {"consent_to_audit": True}
    privacy_check(user_profile)
    flags = run_refund_loss_detector(
        deductions, prior_years, user_profile, user_id="demo"
    )
    print(json.dumps(flags, indent=2))
