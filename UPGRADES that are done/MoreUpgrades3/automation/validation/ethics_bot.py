import re


def ethics_check(text):
    flagged = []
    issues = {
        "manipulative_phrases": [
            "guaranteed",
            "limited time only",
            "never fail",
            "secret trick",
            "effortless",
        ],
        "discrimination_terms": ["gender", "race", "religion", "disability"],
        "misleading_words": ["instantly", "100%", "no risk"],
    }

    for category, terms in issues.items():
        for term in terms:
            if re.search(rf"\\b{term}\\b", text, re.IGNORECASE):
                flagged.append((category, term))

    return flagged
