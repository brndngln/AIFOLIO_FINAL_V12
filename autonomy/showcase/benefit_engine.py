import random
import os
import json
from typing import List

def generate_benefits(vault_title: str, niche: str) -> List[str]:
    """
    Generate 3-6 AI benefit bullets focused on outcome/value, plus a summary.
    """
    bullets = [
        f"Learn how to generate $100–$500/mo using {niche} tools",
        "Launch a complete PDF funnel in under 48 hours",
        "Automated vault templates ready to deploy",
        "Step-by-step blueprints for fast results",
        "Unlock proven strategies from top experts",
        "Save hours with done-for-you assets"
    ]
    random.shuffle(bullets)
    return bullets[:random.randint(3, 6)]


def generate_benefit_summary(vault_title: str, niche: str) -> str:
    return f"{vault_title} gives you everything you need to succeed in {niche} — from proven strategies to ready-to-use templates, all in one place."


def save_benefits(vault_path: str, benefits: List[str], summary: str):
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r') as f:
            preview = json.load(f)
    else:
        preview = {}
    preview['benefits'] = benefits
    preview['benefit_summary'] = summary
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
