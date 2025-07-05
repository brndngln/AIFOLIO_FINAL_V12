import os
import requests


def send_siem_alert(alert_msg):
    webhook_url = os.environ.get("EMMA_SIEM_WEBHOOK")
    if not webhook_url:
        print("No webhook set. Set EMMA_SIEM_WEBHOOK env var.")
        return
    try:
        resp = requests.post(webhook_url, json={"alert": alert_msg})
        print(f"SIEM/webhook status: {resp.status_code}")
    except Exception as e:
        print(f"SIEM/webhook failed: {e}")


if __name__ == "__main__":
    send_siem_alert("Test alert: OMNIELITE intrusion event detected.")
