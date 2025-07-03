import os
import json
import datetime

ANALYZER_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/auto_audit_log_analyzer_log.jsonl'))
os.makedirs(os.path.dirname(ANALYZER_LOG), exist_ok=True)

# --- Analyzer ---
def analyze_audit_log(audit_log_path):
    if not os.path.exists(audit_log_path):
        return {}
    errors = {}
    model_versions = {}
    refund_spikes = {}
    with open(audit_log_path) as f:
        for line in f:
            entry = json.loads(line)
            # Error detection
            if 'error' in entry:
                errors.setdefault(entry['error'], 0)
                errors[entry['error']] += 1
            # Model version drift
            if 'ai_version' in entry:
                v = entry['ai_version']
                model_versions.setdefault(v, 0)
                model_versions[v] += 1
            # Refund risk spikes
            if 'refund_risk' in entry and entry['refund_risk'] == 'high':
                ts = entry.get('timestamp', '')[:7]
                refund_spikes.setdefault(ts, 0)
                refund_spikes[ts] += 1
    summary = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'errors': errors,
        'model_versions': model_versions,
        'refund_spikes': refund_spikes
    }
    with open(ANALYZER_LOG, 'a') as f:
        f.write(json.dumps(summary) + '\n')
    return summary

if __name__ == "__main__":
    # Example usage
    print(analyze_audit_log('../../analytics/ai_performance_log.jsonl'))
