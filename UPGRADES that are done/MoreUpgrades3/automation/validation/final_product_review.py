from .ethics_bot import ethics_check
from .legal_review import legal_review
from .product_qa import quality_guard
from .ethics_fix_bot import auto_fix_ethics_issues

def review_product(content, category):
    log = {
        "ethics_issues": ethics_check(content),
        "legal_issues": legal_review(content, category),
        "qa_report": quality_guard(content)
    }

    # Automatically fix unethical text if issues are found
    if log["ethics_issues"]:
        content = auto_fix_ethics_issues(content)

    # Apply status level
    if log["ethics_issues"] or log["legal_issues"]:
        log["status"] = "WARN"
    elif log["qa_report"]["readability_score"] < 50:
        log["status"] = "WARN"
    else:
        log["status"] = "PASS"

    return log, content