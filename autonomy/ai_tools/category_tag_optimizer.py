import json
import datetime
import os

CAT_TAG_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/category_tag_optimizer_log.jsonl"
    )
)
os.makedirs(os.path.dirname(CAT_TAG_LOG), exist_ok=True)

# --- AI Static Category/Tag Optimizer ---
CATEGORY_KEYWORDS = {
    "business": ["finance", "marketing", "sales", "startup"],
    "creative": ["design", "art", "writing", "music"],
    "education": ["learning", "course", "tutorial", "study"],
    "digital": ["pdf", "ebook", "template", "asset"],
}

TAG_POOL = [
    "productivity",
    "growth",
    "strategy",
    "branding",
    "automation",
    "leadership",
    "innovation",
    "learning",
    "creative",
    "pdf",
    "ebook",
]


def optimize_category_tags(description, keywords=None):
    text = (description or "").lower()
    categories = set()
    tags = set()
    for cat, kw_list in CATEGORY_KEYWORDS.items():
        for kw in kw_list:
            if kw in text:
                categories.add(cat)
    for tag in TAG_POOL:
        if tag in text:
            tags.add(tag)
    if keywords:
        for kw in keywords:
            for cat, kw_list in CATEGORY_KEYWORDS.items():
                if kw in kw_list:
                    categories.add(cat)
            if kw in TAG_POOL:
                tags.add(kw)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "description": description,
        "keywords": keywords,
        "categories": list(categories),
        "tags": list(tags),
    }
    with open(CAT_TAG_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return list(categories), list(tags)
