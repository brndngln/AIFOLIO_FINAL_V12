import random
import os
import json

def generate_review_stats(vault_title: str, vault_quality: float) -> dict:
    """
    Generate star rating, total reviews (10-40), and a featured review.
    """
    avg_rating = round(random.uniform(4.6, 4.9), 1)
    total_reviews = random.randint(10, 40)
    featured_review = random.choice([
        f"Finally a blueprint that works! This paid for itself in 2 days.",
        f"{vault_title} is the real deal. I wish I found this sooner!",
        f"Helped me {random.choice(['get clients', 'launch my offer', 'save time'])} in a week!"
    ])
    return {
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,
        "featured_review": featured_review
    }


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
