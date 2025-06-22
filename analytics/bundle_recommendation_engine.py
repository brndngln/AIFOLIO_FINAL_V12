import json
import datetime
import os

BUNDLE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bundle_recommendation_engine_log.jsonl'))
os.makedirs(os.path.dirname(BUNDLE_LOG), exist_ok=True)

# --- AI Static Bundle Recommendation Engine (Suggest-Only) ---
def recommend_bundles(vault_id, purchase_history):
    # Simple static: suggest bundles if user bought >1 vault in same category
    category_counts = {}
    for p in purchase_history:
        if p['vault_id'] == vault_id:
            cat = p.get('category')
            if cat:
                category_counts[cat] = category_counts.get(cat, 0) + 1
    suggestions = [cat for cat, count in category_counts.items() if count > 1]
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'suggestions': suggestions
    }
    with open(BUNDLE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return suggestions
