import json
import datetime
import os

TAG_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/tag_category_suggester_log.jsonl'))
os.makedirs(os.path.dirname(TAG_LOG), exist_ok=True)

# --- AI Tag & Category Suggestion Engine (Static, No Learning) ---
COMMON_TAGS = ['productivity', 'business', 'finance', 'design', 'marketing', 'education', 'creative', 'pdf', 'ebook']

CATEGORY_MAP = {
    'finance': 'Business',
    'marketing': 'Business',
    'design': 'Creative',
    'education': 'Learning',
    'pdf': 'Digital',
    'ebook': 'Digital',
}

def suggest_tags_categories(description, keywords=None):
    tags = []
    categories = set()
    text = description.lower()
    for tag in COMMON_TAGS:
        if tag in text:
            tags.append(tag)
            if tag in CATEGORY_MAP:
                categories.add(CATEGORY_MAP[tag])
    if keywords:
        for kw in keywords:
            if kw in COMMON_TAGS and kw not in tags:
                tags.append(kw)
                if kw in CATEGORY_MAP:
                    categories.add(CATEGORY_MAP[kw])
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'description': description,
        'tags': tags,
        'categories': list(categories)
    }
    with open(TAG_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return tags, list(categories)
