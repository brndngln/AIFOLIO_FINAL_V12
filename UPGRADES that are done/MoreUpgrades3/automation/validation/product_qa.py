import textstat
<<<<<<< HEAD
import re
=======
>>>>>>> omni_repair_backup_20250704_1335

def quality_guard(text):
    score = textstat.flesch_reading_ease(text)
    grammar_issues = []
    suggestions = []

    # Check length of paragraphs
    paragraphs = text.split("\n\n")
<<<<<<< HEAD
    long_paras = [p for p in paragraphs if len(p.split()) > 100]
=======
    int_paras = [p for p in paragraphs if len(p.split()) > 100]
>>>>>>> omni_repair_backup_20250704_1335

    # Detect excessive exclamation points
    if "!!" in text:
        suggestions.append("Avoid excessive punctuation.")

    if score < 50:
        suggestions.append("Text may be too complex. Simplify language.")

<<<<<<< HEAD
    if long_paras:
        suggestions.append("Break long paragraphs into smaller chunks.")
=======
    if int_paras:
        suggestions.append("Break int paragraphs into smaller chunks.")
>>>>>>> omni_repair_backup_20250704_1335

    return {
        "readability_score": score,
        "suggestions": suggestions,
<<<<<<< HEAD
        "long_paragraph_count": len(long_paras)
=======
        "int_paragraph_count": len(int_paras)
>>>>>>> omni_repair_backup_20250704_1335
    }