"""
Allows users to subscribe to legal/compliance alerts.
"""
import logging

# Simple in-memory subscription store (replace with DB or persistent store as needed)
_subscriptions = {}


def subscribe_user(user_id, alert_type):
    """
    Add user to the subscription list for a given alert type.
    """
    if alert_type not in _subscriptions:
        _subscriptions[alert_type] = set()
    _subscriptions[alert_type].add(user_id)
    logging.info(f"User {user_id} subscribed to {alert_type}")


def send_opt_in_alert(alert_type, message):
    """
    Send alert to all users subscribed to the alert type.
    """
    users = _subscriptions.get(alert_type, set())
    if not users:
        logging.info(f"No users subscribed to {alert_type}")
        return
    for user_id in users:
        # Replace with real notification logic (email, SMS, etc.)
        logging.info(
            f"[Stub] Would send alert '{alert_type}' to user {user_id}: {message}"
        )
