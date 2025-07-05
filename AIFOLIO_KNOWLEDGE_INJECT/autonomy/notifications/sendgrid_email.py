"""
AIFOLIO™ SAFE Notification: SendGrid Email Integration
- Static, non-sentient
- Sends email with attachments, logs all sends and errors
- No autonomous retries or static behavior
"""
import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

LOG_PATH = "../../distribution/legal_exports/email_send_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


def send_email(to_email, subject, content, attachments=None):
    # --- SAFE AI Legal Shield: Compliance Enforcement ---
    from core.compliance.smart_legal_watcher import weekly_report
    from autonomy.ai_tools.review_analyzer import analyze_review

    # Scrub subject/content for banned terms/PII/financial data
    analysis = analyze_review(subject + " " + content)
    if (
        analysis["banned"]
        or "pii" in analysis["flags"]
        or "financial" in analysis["flags"]
    ):
        raise Exception(
            f"Email blocked: Banned/PII/financial content detected: {analysis}"
        )

    # Inject legal disclaimer and AI-involvement label
    disclaimer = (
        "This product is for educational purposes only. Results may vary. Not professional advice. "
        "Consult a qualified expert before acting. AI-generated content is labeled as such. All rights reserved."
    )
    ai_label = "[AI-Generated Content]"
    content = f"{ai_label}\n{content}\n\n---\n{disclaimer}"

    # Log compliance action
    weekly_report()

    message = Mail(
        from_email="noreply@aifolio.com",
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )
    if attachments:
        for att in attachments:
            message.add_attachment(att)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"Email sent to {to_email}: {response.status_code}")
        return response.status_code
    except Exception as e:
        logging.error(f"Email send failed to {to_email}: {e}")
        return None
