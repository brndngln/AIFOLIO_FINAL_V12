import json
import datetime
import os

OPP_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/market_opportunity_analyzer_log.jsonl'))
os.makedirs(os.path.dirname(OPP_LOG), exist_ok=True)

# --- AI Market Opportunity Analyzer (Read-Only) ---
def analyze_market_opportunities(category_stats):
    # Example: flag categories with high demand/low supply
    opportunities = []
    for cat, stats in category_stats.items():
        if stats['demand'] > 100 and stats['supply'] < 20:
            opportunities.append(cat)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'opportunities': opportunities
    }
    with open(OPP_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return opportunities
