import os
import logging
import requests

def notify_internal_channels(order_id):
    """
    Notify internal channels (Slack/Discord) about the sale using webhooks from environment variables.
    """
    slack_url = os.environ.get('SLACK_WEBHOOK_URL')
    discord_url = os.environ.get('DISCORD_WEBHOOK_URL')
    message = f"AIFOLIO: New order {order_id} completed."
    sent = False
    try:
        if slack_url:
            resp = requests.post(slack_url, json={'text': message}, timeout=5)
            if resp.status_code == 200:
                logging.info(f"[AIFOLIO] Slack notified for order {order_id}.")
                sent = True
            else:
                logging.error(f"[AIFOLIO] Slack webhook error: {resp.status_code} {resp.text}")
        if discord_url:
            resp = requests.post(discord_url, json={'content': message}, timeout=5)
            if resp.status_code == 204:
                logging.info(f"[AIFOLIO] Discord notified for order {order_id}.")
                sent = True
            else:
                logging.error(f"[AIFOLIO] Discord webhook error: {resp.status_code} {resp.text}")
        if not sent:
            print(f"[AIFOLIO] Internal channels notified for order {order_id} (stub, no webhook set)")
    except Exception as e:
        logging.error(f"[AIFOLIO] Exception notifying internal channels: {e}")
