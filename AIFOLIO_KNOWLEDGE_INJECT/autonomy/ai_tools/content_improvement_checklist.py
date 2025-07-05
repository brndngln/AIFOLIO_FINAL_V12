import json
import datetime
import os

CHECKLIST_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../analytics/content_improvement_checklist_log.jsonl",
    )
)
os.makedirs(os.path.dirname(CHECKLIST_LOG), exist_ok=True)


# --- AI Static Content Improvement Checklist (Suggest-Only) ---
def content_checklist(text):
    suggestions = []
    if len(text) < 100:
        suggestions.append("Content is short; consider expanding.")
    if not text.endswith("."):
        suggestions.append("Content should end with a period.")
    if text and text[0].islower():
        suggestions.append("Content should start with a capital letter.")
    if "http" in text:
        suggestions.append("Check for broken or outdated links.")
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "text": text,
        "suggestions": suggestions,
    }
    with open(CHECKLIST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return suggestions
