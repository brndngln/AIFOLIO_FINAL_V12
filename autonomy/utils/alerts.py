def send_slack_alert(msg):
    print(f"[SLACK ALERT] {msg}")

def send_telegram_alert(msg):
    print(f"[TELEGRAM ALERT] {msg}")

def send_email_alert(email, msg):
    print(f"[EMAIL ALERT to {email}] {msg}")
