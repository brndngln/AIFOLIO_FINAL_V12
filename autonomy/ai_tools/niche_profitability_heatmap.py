import json
import datetime
import os

HEATMAP_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/niche_profitability_heatmap_log.jsonl'))
os.makedirs(os.path.dirname(HEATMAP_LOG), exist_ok=True)

# --- AI Niche Profitability Heatmap (Visualization Only) ---
def generate_heatmap(niche_stats):
    # Example: create a simple data structure for visualization
    heatmap = {niche: stats['profit'] for niche, stats in niche_stats.items()}
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'heatmap': heatmap
    }
    with open(HEATMAP_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return heatmap
