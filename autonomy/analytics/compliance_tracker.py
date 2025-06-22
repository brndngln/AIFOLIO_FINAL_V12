"""
AIFOLIO SAFE AI Compliance Tracker (static, non-sentient)
- Tracks % of orders with legal policy, policy confirmations, receipts delivered
- All actions logged to analytics_log.json
"""
import json
import os

COMP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compliance_tracker.json'))
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'analytics_log.json'))

def track_compliance(orders):
    total = len(orders)
    with_policy = sum(1 for o in orders if o.get('has_policy'))
    confirmed = sum(1 for o in orders if o.get('policy_confirmed'))
    receipts = sum(1 for o in orders if o.get('receipt_delivered'))
    stats = {
        'total_orders': total,
        'percent_with_policy': (with_policy / total) * 100 if total else 0,
        'percent_confirmed': (confirmed / total) * 100 if total else 0,
        'percent_receipts': (receipts / total) * 100 if total else 0
    }
    with open(COMP_PATH, 'w') as f:
        json.dump(stats, f, indent=2)
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps({'action': 'track_compliance', 'stats': stats}) + '\n')
    return stats
