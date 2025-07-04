import os
import logging
import requests
import json

def push_to_dashboard_analytics(order_id):
    """
    POST order analytics to DASHBOARD_ANALYTICS_URL if set, else log to file. Add error handling and logging.
    """
    api_url = os.environ.get('DASHBOARD_ANALYTICS_URL')
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/dashboard_analytics.json'))
    entry = {'order_id': order_id}
    try:
        if api_url:
            resp = requests.post(api_url, json=entry, timeout=10)
            if resp.status_code == 200:
                logging.info(f"[AIFOLIO] Dashboard analytics API success for order {order_id}.")
            else:
                logging.error(f"[AIFOLIO] Dashboard analytics API error: {resp.status_code} {resp.text}")
        else:
            if os.path.exists(log_path):
                with open(log_path, 'r+') as f:
                    logs = json.load(f)
                    logs.append(entry)
                    f.seek(0)
                    json.dump(logs, f, indent=2)
            else:
                with open(log_path, 'w') as f:
                    json.dump([entry], f, indent=2)
            print(f"[AIFOLIO] Dashboard analytics logged for order {order_id} (no DASHBOARD_ANALYTICS_URL)")
    except Exception as e:
        logging.error(f"[AIFOLIO] Exception posting dashboard analytics: {e}")
