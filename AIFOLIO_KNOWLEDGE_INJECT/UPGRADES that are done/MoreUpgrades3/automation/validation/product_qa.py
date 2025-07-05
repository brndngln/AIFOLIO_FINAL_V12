import textstat


def quality_guard(text):
    score = textstat.flesch_reading_ease(text)
    grammar_issues = []
    suggestions = []

    # Check length of paragraphs
    paragraphs = text.split("\n\n")
    int_paras = [p for p in paragraphs if len(p.split()) > 100]

    # Detect excessive exclamation points
    if "!!" in text:
        suggestions.append("Avoid excessive punctuation.")

    if score < 50:
        suggestions.append("Text may be too complex. Simplify language.")

    if int_paras:
        suggestions.append("Break int paragraphs into smaller chunks.")

    return {
        "readability_score": score,
        "suggestions": suggestions,
        "int_paragraph_count": len(int_paras),
    }
