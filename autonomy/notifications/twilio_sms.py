"""
AIFOLIO™ SAFE Notification: Twilio SMS Integration
- Static, non-sentient
- Sends SMS, logs all sends and errors
- No autonomous retries or static behavior
"""
import os
import logging
from twilio.rest import Client

LOG_PATH = "../../distribution/legal_exports/sms_send_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM_NUMBER")


def send_sms(to_number, message):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=to_number
        )
        logging.info(f"SMS sent to {to_number}: {msg.sid}")
        return msg.sid
    except Exception as e:
        logging.error(f"SMS send failed to {to_number}: {e}")
        return None
