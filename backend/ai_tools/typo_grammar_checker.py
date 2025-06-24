"""
AIFOLIO SAFE AI Typo/Grammar Checker
Static, deterministic checker for marketing copy and vault content.
All suggestions require human review. No learning or adaptation.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_COMMON_ERRORS = [
    ("teh", "the"),
    ("recieve", "receive"),
    ("occurence", "occurrence"),
    ("definately", "definitely"),
    ("seperate", "separate"),
    ("adress", "address")
]

def check_typos_and_grammar(text: str) -> list:
    """Deterministic, static typo/grammar checker. Extension: real grammar API."""
    issues = []
    for typo, correction in STATIC_COMMON_ERRORS:
        if typo in text:
            issues.append({
                'error': typo,
                'suggestion': correction,
                'type': 'typo',
                'requires_human_review': True
            })
    logger.info(f"Checked text for typos/grammar. Issues: {issues}")
    return issues
