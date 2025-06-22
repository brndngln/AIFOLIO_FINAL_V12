import os
import json
import datetime
import pandas as pd
from textblob import TextBlob

REFUND_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/gumroad_refund_log.jsonl'))
os.makedirs(os.path.dirname(REFUND_LOG), exist_ok=True)

# --- Refund Reason Sentiment Scanner ---
def log_refund(product_id, reason_text, amount):
    sentiment = TextBlob(reason_text).sentiment.polarity
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'product_id': product_id,
        'reason': reason_text,
        'sentiment': sentiment,
        'amount': amount
    }
    with open(REFUND_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

def refund_probability(product_id):
    if not os.path.exists(REFUND_LOG):
        return 0.0
    data = [json.loads(line) for line in open(REFUND_LOG)]
    df = pd.DataFrame(data)
    prod = df[df['product_id'] == product_id]
    if prod.empty:
        return 0.0
    # Simple: refund rate = count / total
    refund_rate = len(prod) / max(1, len(df[df['product_id'] == product_id]))
    # If many negative sentiments, increase risk
    neg_count = (prod['sentiment'] < -0.3).sum()
    risk = refund_rate + 0.1 * neg_count
    return min(1.0, risk)

def refund_trends():
    if not os.path.exists(REFUND_LOG):
        return {}
    data = [json.loads(line) for line in open(REFUND_LOG)]
    df = pd.DataFrame(data)
    trends = df.groupby(df['timestamp'].str[:7]).size().to_dict()
    return trends

if __name__ == "__main__":
    log_refund('prod_1', 'Customer said content was too basic.', 49)
    print(refund_probability('prod_1'))
    print(refund_trends())
