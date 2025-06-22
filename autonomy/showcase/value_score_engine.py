import os
import json

def compute_value_score(metadata: dict, outline: list) -> int:
    """
    Assigns a value score (0–100) based on page length, outline, niche, bundle size, and clarity.
    """
    score = 50
    page_count = metadata.get('page_count', 0)
    score += min(page_count, 40)
    score += min(len(outline) * 2, 10)
    if metadata.get('niche') in ['ai', 'money', 'investing']:
        score += 10
    if metadata.get('bundle_size', 1) > 1:
        score += 10
    # AI-detected clarity/structure stub: always add +10 for now
    score += 10
    return min(score, 100)


def save_value_score(vault_path: str, value_score: int):
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r') as f:
            preview = json.load(f)
    else:
        preview = {}
    preview['value_score'] = value_score
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
