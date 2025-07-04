import os
import json
import datetime
import pandas as pd

NICHE_DISCOVERY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_niche_discovery_log.jsonl'))
os.makedirs(os.path.dirname(NICHE_DISCOVERY_LOG), exist_ok=True)

# --- Niche Discovery Engine ---
def discover_niches(sales_log, refund_log):
    # Load sales data
    if not os.path.exists(sales_log) or not os.path.exists(refund_log):
        return {}
    sales = [json.loads(line) for line in open(sales_log)]
    refunds = [json.loads(line) for line in open(refund_log)]
    df_sales = pd.DataFrame(sales)
    df_refunds = pd.DataFrame(refunds)
    # Trend analysis
    by_niche = df_sales.groupby('niche').size().sort_values(ascending=False)
    by_refund = df_refunds.groupby('niche').size().sort_values(ascending=False)
    emerging = by_niche.head(3).index.tolist()
    declining = by_refund.head(3).index.tolist()
    micro_niches = [n for n in by_niche.index if by_niche[n] < 5 and n not in emerging]
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'emerging_niches': emerging,
        'declining_niches': declining,
        'micro_niches': micro_niches
    }
    with open(NICHE_DISCOVERY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

if __name__ == "__main__":
    print(discover_niches('../../analytics/niche_performance_log.jsonl', '../../analytics/gumroad_refund_log.jsonl'))
