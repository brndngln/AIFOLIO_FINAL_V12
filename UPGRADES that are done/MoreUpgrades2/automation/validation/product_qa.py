import textstat
import re

def quality_guard(text):
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

    return {
        "readability_score": score,
        "suggestions": suggestions,
        "long_paragraph_count": len(long_paras)
    }