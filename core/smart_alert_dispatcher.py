# smart_alert_dispatcher.py
# Sends push, email, and dashboard alerts for purchases and reinvestments
class SmartAlertDispatcher:
    def __init__(self, channels: list[str]) -> None:
        self.channels: list[str] = channels

    def send_alert(self, alert: str) -> None:
        for channel in self.channels:
            # Integrate with real push/email/discord/telegram APIs
            print(f"[ALERT:{channel}] {alert}")
