import os
import json
import logging

POST_SALE_HOOKS_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/post_sale_hooks.log'))

# --- Admin UI Data Provider ---
def get_failed_hooks():
    """
    Parses the post_sale_hooks.log and returns a list of failed hook executions.
    Each entry: { 'hook': str, 'error': str, 'context': dict, 'timestamp': str }
    """
    failed = []
    if not os.path.exists(POST_SALE_HOOKS_LOG):
        return failed
    with open(POST_SALE_HOOKS_LOG, 'r') as f:
        for line in f:
            if '[ERROR]' in line:
                # Example: [ERROR] hook_name: error | Context: {...}
                try:
                    prefix, rest = line.split('] ', 1)
                    hook_part, context_part = rest.split('| Context: ', 1)
                    hook_name, error = hook_part.split(': ', 1)
                    context = json.loads(context_part.strip().replace("'", '"')) if '{' in context_part else {}
                    failed.append({
                        'hook': hook_name.replace('[ERROR] ', '').strip(),
                        'error': error.strip(),
                        'context': context,
                        'timestamp': prefix.replace('[', '').strip()
                    })
                except Exception as e:
                    logging.warning(f"Failed to parse log line: {line} | {e}")
    return failed

# --- CLI/Programmatic Replay ---
def replay_failed_hooks():
    """
    CLI or programmatic replay of failed hooks.
    Re-runs failed hooks with their original context.
    """
    failed = get_failed_hooks()
    if not failed:
        print("No failed hooks to replay.")
        return
    for entry in failed:
        hook = entry['hook']
        context = entry['context']
        print(f"Replaying {hook} with context: {context}")
        try:
            # Dynamically import and call the hook
            mod = __import__(f"autonomy.post_sale_hooks.{hook}", fromlist=[hook])
            func = getattr(mod, hook)
            if isinstance(context, dict):
                func(**context)
            else:
                func(context)
        except Exception as e:
            logging.error(f"Replay failed for {hook}: {e}")

# --- External Alerting (Slack/Discord/PagerDuty) ---
import os
import requests

def send_alert(message, service='slack'):
    """
    Send an alert to Slack, Discord, or PagerDuty using webhooks.
    Webhook URLs are read from environment variables:
      SLACK_WEBHOOK_URL, DISCORD_WEBHOOK_URL, PAGERDUTY_WEBHOOK_URL
    """
    print(f"[ALERT-{service.upper()}] {message}")
    webhook_env = {
        'slack': 'SLACK_WEBHOOK_URL',
        'discord': 'DISCORD_WEBHOOK_URL',
        'pagerduty': 'PAGERDUTY_WEBHOOK_URL'
    }
    url = os.environ.get(webhook_env.get(service, ''), None)
    if not url:
        print(f"[ALERT-{service.upper()}] Webhook URL not set in environment.")
        return
    payload = {'text': message} if service == 'slack' else {'content': message}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code != 200:
            print(f"[ALERT-{service.upper()}] Failed to send alert: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[ALERT-{service.upper()}] Exception sending alert: {e}")
