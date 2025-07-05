import re


def auto_fix_ethics_issues(text):
    issues = {
        "guaranteed": "can help improve",
        "never fail": "offers consistent support",
        "secret trick": "lesser-known technique",
        "100%": "highly likely",
        "instantly": "quickly",
        "effortless": "simple to follow",
    }

    for bad, replacement in issues.items():
        text = re.sub(rf"\\b{bad}\\b", replacement, text, flags=re.IGNORECASE)

    return text
