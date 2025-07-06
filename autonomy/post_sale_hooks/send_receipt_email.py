import os
import logging
import requests
import json


def send_receipt_email(order_id: str, user_email: str) -> None:
    """
    Send a receipt email via SendGrid if configured, else log to file. Add error handling and logging.
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@aifolio.com")
    subject = f"Your AIFOLIO Receipt for Order {order_id}"
    body = f"Thank you for your purchase! Here is your receipt for order {order_id}."
    log_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../analytics/receipt_emails.json")
    )
    entry = {"order_id": order_id, "user_email": user_email}
    try:
        if api_key:
            resp = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": user_email}]}],
                    "from": {"email": sender},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}],
                },
                timeout=10,
            )
            if resp.status_code == 202:
                logging.info(
                    f"[AIFOLIO] Receipt email sent to {user_email} for order {order_id}."
                )
            else:
                logging.error(
                    f"[AIFOLIO] Failed to send receipt email: {resp.status_code} {resp.text}"
                )
        else:
            if os.path.exists(log_path):
                with open(log_path, "r+") as f:
                    logs = json.load(f)
                    logs.append(entry)
                    f.seek(0)
                    json.dump(logs, f, indent=2)
            else:
                with open(log_path, "w") as f:
                    json.dump([entry], f, indent=2)
            print(
                f"[AIFOLIO] Receipt email logged for {user_email} (no SENDGRID_API_KEY)"
            )
    except Exception as e:
        logging.error(f"[AIFOLIO] Exception sending receipt email: {e}")
