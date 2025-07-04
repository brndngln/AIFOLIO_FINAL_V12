import pandas as pd
import json
import os
import datetime

PROFIT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/profitability_optimizer_log.jsonl'))
os.makedirs(os.path.dirname(PROFIT_LOG), exist_ok=True)

# --- Profitability Optimizer Dashboard ---
def compute_profitability(sales, refunds, costs):
    """
    Computes vault-level and overall ROI, logs audit entry.
    sales: list of dicts {vault, amount, timestamp}
    refunds: list of dicts {vault, amount, timestamp}
    costs: dict {vault: cost}
    Returns: dict of vault-level and overall ROI
    """
    df_sales = pd.DataFrame(sales)
    df_refunds = pd.DataFrame(refunds)
    vaults = set(df_sales['vault']).union(df_refunds['vault'])
    result = {}
    for v in vaults:
        sales_amt = df_sales[df_sales['vault']==v]['amount'].sum()
        refund_amt = df_refunds[df_refunds['vault']==v]['amount'].sum() if not df_refunds.empty else 0
        cost = costs.get(v, 0)
        profit = sales_amt - refund_amt - cost
        roi = (profit / cost) if cost else None
        result[v] = {'sales': sales_amt, 'refunds': refund_amt, 'cost': cost, 'profit': profit, 'roi': roi}
    overall = {'sales': df_sales['amount'].sum(), 'refunds': df_refunds['amount'].sum() if not df_refunds.empty else 0, 'cost': sum(costs.values())}
    overall['profit'] = overall['sales'] - overall['refunds'] - overall['cost']
    overall['roi'] = (overall['profit']/overall['cost']) if overall['cost'] else None
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vaults': result,
        'overall': overall
    }
    with open(PROFIT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return {'vaults': result, 'overall': overall}

if __name__ == "__main__":
    print(compute_profitability([
        {'vault': 'v1', 'amount': 100, 'timestamp': '2025-06-21'},
        {'vault': 'v2', 'amount': 200, 'timestamp': '2025-06-21'}
    ], [
        {'vault': 'v1', 'amount': 10, 'timestamp': '2025-06-21'}
    ], {'v1': 50, 'v2': 80}))
