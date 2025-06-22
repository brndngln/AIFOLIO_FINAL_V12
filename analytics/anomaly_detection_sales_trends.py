import json
import datetime
import os

ANOMALY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'anomaly_detection_sales_trends_log.jsonl'))
os.makedirs(os.path.dirname(ANOMALY_LOG), exist_ok=True)

# --- AI Anomaly Detection on Sales Trends (Static) ---
def detect_sales_anomaly(vault_id, sales):
    # Simple static rule: flag if sales drop >50% week-over-week
    sales_by_week = {}
    for s in sales:
        dt = datetime.datetime.fromisoformat(s['timestamp'].replace('Z',''))
        week = dt.isocalendar()[1]
        sales_by_week.setdefault(week, 0)
        sales_by_week[week] += 1
    weeks = sorted(sales_by_week.keys())
    anomaly = False
    details = {}
    if len(weeks) >= 2:
        last, prev = sales_by_week[weeks[-1]], sales_by_week[weeks[-2]]
        if prev > 0 and last < prev * 0.5:
            anomaly = True
            details = {'prev_week': prev, 'last_week': last}
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'anomaly': anomaly,
        'details': details
    }
    with open(ANOMALY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return anomaly, details
