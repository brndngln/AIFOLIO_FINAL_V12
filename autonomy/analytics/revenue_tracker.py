"""
AIFOLIO SAFE AI Revenue Tracker (static, non-sentient)
- Tracks total revenue by time period, vault, niche
- Refund-adjusted totals
- All actions logged to analytics_log.json
"""
import json
import os
import datetime

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'analytics_log.json'))


def track_revenue(sales, refunds):
    now = datetime.datetime.utcnow()
    periods = {
        'all_time': None,
        'this_month': now.strftime('%Y-%m'),
        'last_30_days': (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    }
    totals = {'all_time': 0, 'this_month': 0, 'last_30_days': 0, 'by_vault': {}, 'by_niche': {}}
    for s in sales:
        totals['all_time'] += s['amount']
        if s['date'].startswith(periods['this_month']):
            totals['this_month'] += s['amount']
        if s['date'] >= periods['last_30_days']:
            totals['last_30_days'] += s['amount']
        v = s['vault_id']
        totals['by_vault'].setdefault(v, 0)
        totals['by_vault'][v] += s['amount']
        n = s.get('niche', 'unknown')
        totals['by_niche'].setdefault(n, 0)
        totals['by_niche'][n] += s['amount']
    for r in refunds:
        totals['all_time'] -= r['amount']
        if r['date'].startswith(periods['this_month']):
            totals['this_month'] -= r['amount']
        if r['date'] >= periods['last_30_days']:
            totals['last_30_days'] -= r['amount']
        v = r['vault_id']
        totals['by_vault'][v] -= r['amount']
        n = r.get('niche', 'unknown')
        totals['by_niche'][n] -= r['amount']
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps({'action': 'track_revenue', 'totals': totals}) + '\n')
    return totals
