import os
import requests
import logging

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

logger = logging.getLogger("alert_engine")

def send_alert(type="compliance_failure", method="email", message="Vault failed PDF compliance check.", to=None):
    if method == "email" and SENDGRID_API_KEY:
        data = {
            "personalizations": [{"to": [{"email": to or "admin@aifolio.com"}]}],
            "from": {"email": "alerts@aifolio.com"},
            "subject": f"AIFOLIO Alert: {type}",
            "content": [{"type": "text/plain", "value": message}]
        }
        r = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": f"Bearer {SENDGRID_API_KEY}", "Content-Type": "application/json"},
            json=data
        )
        logger.info(f"SendGrid alert: {r.status_code}")
    elif method == "sms" and TWILIO_SID and TWILIO_TOKEN:
        requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
            data={"To": to, "From": os.getenv("TWILIO_FROM"), "Body": message},
            auth=(TWILIO_SID, TWILIO_TOKEN)
        )
        logger.info(f"Twilio SMS alert sent to {to}")
    elif method == "slack" and SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        logger.info("Slack alert sent.")
    elif method == "discord" and DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        logger.info("Discord alert sent.")
    else:
        logger.warning(f"No alert method or API key for {method}.")
