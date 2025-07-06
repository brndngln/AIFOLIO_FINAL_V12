# Emma Compliance Lock
OWNER_LOCK = True
import os
import smtplib
import json
import datetime
from email.mime.text import MIMEText
from email.utils import formataddr

EMAIL_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/email_alert_log.jsonl")
)
os.makedirs(os.path.dirname(EMAIL_LOG), exist_ok=True)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "AIFOLIO Vaults")


# --- Opt-in Email Alerts for Vault Builds ---
def send_vault_email_alert(to_email: str, subject: str, body: str) -> None:
    # --- SAFE AI Legal Shield: Compliance Enforcement ---
    from core.compliance.smart_legal_watcher import weekly_report
    from autonomy.ai_tools.review_analyzer import analyze_review

    # Scrub subject/body for banned terms/PII/financial data
    analysis = analyze_review(subject + " " + body)  # type: ignore[no-untyped-call]
    if (
        analysis["banned"]
        or "pii" in analysis["flags"]
        or "financial" in analysis["flags"]
    ):
        raise Exception(
            f"Vault email blocked: Banned/PII/financial content detected: {analysis}"
        )

    # Inject legal disclaimer and AI-involvement label
    disclaimer = (
        "This product is for educational purposes only. Results may vary. Not professional advice. "
        "Consult a qualified expert before acting. AI-generated content is labeled as such. All rights reserved."
    )
    ai_label = "[AI-Generated Content]"
    body = f"{ai_label}\n{body}\n\n---\n{disclaimer}"

    # Log compliance action
    weekly_report()

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    from typing import cast
    from typing import cast
    msg["From"] = formataddr((cast(str, FROM_NAME) if FROM_NAME is not None else None, cast(str, FROM_EMAIL)))
    msg["To"] = to_email
    try:
        with smtplib.SMTP(cast(str, SMTP_HOST), SMTP_PORT) as server:
            server.starttls()
            server.login(cast(str, SMTP_USER), cast(str, SMTP_PASS))
            server.send_message(msg)
        status = "sent"
    except Exception as e:
        status = f"error: {e}"
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "to": to_email,
        "subject": subject,
        "status": status,
    }
    with open(EMAIL_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

