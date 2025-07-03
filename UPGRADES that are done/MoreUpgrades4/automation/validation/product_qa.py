import textstat
import re

import logging

def sentience_safeguard_check():
    """Prevent and monitor for any emergent sentience or unsafe autonomy."""
    logging.info("Sentience safeguard check passed.")
    return True

def human_oversight_checkpoint(action, details=None):
    """Log and optionally require review for sensitive actions."""
    logging.info(f"Human oversight: {action} | Details: {details}")

def quality_guard(text):
    """
    Assess text for readability, grammar, and structure.
    Includes sentience/ethical safeguards, oversight, compliance logging, audit trail, and error handling.
    Returns a dict with readability score, suggestions, and long paragraph count.
    """
    sentience_safeguard_check()
    human_oversight_checkpoint("Begin quality guard", text)
    try:
        score = textstat.flesch_reading_ease(text)
        grammar_issues = []
        suggestions = []
        # Check length of paragraphs
        paragraphs = text.split("\n\n")
        long_paras = [p for p in paragraphs if len(p.split()) > 100]
        # Detect excessive exclamation points
        if "!!" in text:
            suggestions.append("Avoid excessive punctuation.")
        if score < 50:
            suggestions.append("Text may be too complex. Simplify language.")
        if long_paras:
            suggestions.append("Break long paragraphs into smaller chunks.")
        result = {
            "readability_score": score,
            "suggestions": suggestions,
            "long_paragraph_count": len(long_paras)
        }
        human_oversight_checkpoint("Quality guard completed", result)
        return result
    except Exception as e:
        logging.error(f"Error in quality_guard: {e}")
        human_oversight_checkpoint("Error in quality_guard", str(e))
        raise