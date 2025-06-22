import os
import json
import datetime

REFUND_TRIGGER_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/refund_trigger_predictor_log.jsonl'))
os.makedirs(os.path.dirname(REFUND_TRIGGER_LOG), exist_ok=True)

# --- Refund Trigger Predictor ---
def predict_refund_risk(order_id, delivery_status, download_attempts, user_behavior):
    # Simple rules: non-delivery, >3 downloads, suspicious behavior
    risk = 'low'
    if delivery_status != 'delivered':
        risk = 'high'
    elif download_attempts > 3:
        risk = 'medium'
    elif user_behavior == 'suspicious':
        risk = 'high'
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'order_id': order_id,
        'delivery_status': delivery_status,
        'download_attempts': download_attempts,
        'user_behavior': user_behavior,
        'risk': risk
    }
    with open(REFUND_TRIGGER_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

if __name__ == "__main__":
    print(predict_refund_risk('order_1', 'delivered', 1, 'normal'))
    print(predict_refund_risk('order_2', 'failed', 2, 'normal'))
