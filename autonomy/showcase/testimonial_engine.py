import random
import os
import json
from typing import List

PERSONAS = [
    ("Sara T., freelancer"),
    ("Mike B., agency owner"),
    ("Priya S., coach"),
    ("Alex R., student"),
    ("Jordan W., entrepreneur")
]

def generate_testimonials(vault_title: str, niche: str) -> List[dict]:
    """
    Generate 2-3 realistic testimonials per vault, matching niche and outcomes.
    """
    templates = [
        "I never thought {vault} would make such a difference. Now I'm {outcome}!",
        "As a {persona}, this {niche} vault gave me the exact steps I needed.",
        "After using {vault}, I achieved {outcome} in just weeks!"
    ]
    outcomes = [
        "making real progress",
        "earning extra income",
        "feeling confident in my strategy",
        "saving hours each week",
        "launching my own product"
    ]
    testimonials = []
    for i in range(random.randint(2, 3)):
        persona = random.choice(PERSONAS)
        template = random.choice(templates)
        outcome = random.choice(outcomes)
        text = template.format(vault=vault_title, niche=niche, outcome=outcome, persona=persona)
        testimonials.append({"text": text, "persona": persona})
    return testimonials


def save_testimonials(vault_path: str, testimonials: List[dict]):
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r') as f:
            preview = json.load(f)
    else:
        preview = {}
    preview['testimonials'] = testimonials
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
