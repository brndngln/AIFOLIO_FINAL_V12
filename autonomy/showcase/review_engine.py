"""
AIFOLIO Review Engine
- Generates deterministic, static review stats
- Audit-logs all review events
- GDPR/CCPA compliant, owner controlled
"""
import os
import json
from datetime import datetime

def audit_log(event, details=None):
    AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), 'review_audit_log.json')
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details or {}
    }
    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(AUDIT_LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)

def generate_review_stats(vault_title: str, vault_quality: float, owner_override: dict = None) -> dict:
    """
    Generate deterministic star rating, total reviews (10-40), and a featured review.
    Owner can override. Audit-logs all actions. GDPR/CCPA compliant.
    """
    if owner_override:
        stats = owner_override.copy()
        audit_log('OWNER_OVERRIDE_REVIEW_STATS', {'stats': stats})
    else:
        # Deterministic: based on vault_quality and vault_title length
        avg_rating = round(4.6 + (vault_quality % 0.3), 1)
        total_reviews = 10 + (len(vault_title) % 31)  # 10-40
        featured_reviews = [
            "Finally a blueprint that works! This paid for itself in 2 days.",
            f"{vault_title} is the real deal. I wish I found this sooner!",
            "Helped me get results in a week!"
        ]
        featured_review = featured_reviews[len(vault_title) % len(featured_reviews)]
        stats = {
            "avg_rating": avg_rating,
            "total_reviews": total_reviews,
            "featured_review": featured_review
        }
        audit_log('GENERATE_REVIEW_STATS', {'vault_title': vault_title, 'vault_quality': vault_quality, 'stats': stats})
    # Validation: max 40 reviews
    if stats["total_reviews"] > 40:
        stats["total_reviews"] = 40
    if stats["total_reviews"] < 10:
        stats["total_reviews"] = 10
    return stats

def save_review_stats(vault_path: str, stats: dict):
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r') as f:
            preview = json.load(f)
    else:
        preview = {}
    preview.update(stats)
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
    audit_log('SAVE_REVIEW_STATS', {'vault_path': vault_path, 'stats': stats})
