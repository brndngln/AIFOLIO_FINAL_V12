import json
import datetime
import os

PROFIT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vault_profitability_score_log.jsonl'))
os.makedirs(os.path.dirname(PROFIT_LOG), exist_ok=True)

# --- Vault Profitability Score (Static) ---
def calculate_profitability(vault_id, sales, refunds, costs):
    total_sales = sum(s['amount'] for s in sales if s['vault_id'] == vault_id)
    total_refunds = sum(r['amount'] for r in refunds if r['vault_id'] == vault_id)
    total_costs = sum(c['amount'] for c in costs if c['vault_id'] == vault_id)
    profit = total_sales - total_refunds - total_costs
    score = profit / (total_costs + 1)  # Avoid div by zero
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'profit': profit,
        'score': score
    }
    with open(PROFIT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return score
