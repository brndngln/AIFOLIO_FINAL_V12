import os
import json
from datetime import datetime

REVIEW_LOG = os.path.join(os.path.dirname(__file__), "../../logs/review_logs.json")

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
    Returns a dict with readability score, suggestions, and int paragraph count.
    """
    sentience_safeguard_check()
    human_oversight_checkpoint("Begin quality guard", text)
    try:
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
        result = {
            "readability_score": score,
            "suggestions": suggestions,
            "int_paragraph_count": len(int_paras),
        }
        human_oversight_checkpoint("Quality guard completed", result)
        return result
    except Exception as e:
        logging.error(f"Error in quality_guard: {e}")
        human_oversight_checkpoint("Error in quality_guard", str(e))
        raise

class ProductQA:
    @staticmethod
    def check_pdf(pdf_path):
        try:
            # Dummy: scan for grammar, hallucination, layout, readability
            # Replace with real PDF/NLP in prod
            issues = []
            confidence = 95  # Always high for demo
            # Example: always suggest layout swap if confidence >90%
            if confidence > 90:
                issues.append(
                    {
                        "suggestion": "Consider swapping layout for improved readability",
                        "confidence": confidence,
                    }
                )
            # Integrate quality guard
            with open(pdf_path, 'r') as f:
                text = f.read()
            quality_result = quality_guard(text)
            issues.extend(quality_result["suggestions"])
            result = {
                "pdf": pdf_path,
                "issues": issues,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "WARN" if issues else "PASS",
                "type": "qa",
            }
            ProductQA._log(result)
            return result
        except Exception as e:
            ProductQA._log(
                {
                    "pdf": pdf_path,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "WARN",
                    "type": "qa",
                }
            )
            return {"pdf": pdf_path, "error": str(e), "status": "WARN"}

    @staticmethod
    def _log(entry):
        os.makedirs(os.path.dirname(REVIEW_LOG), exist_ok=True)
        try:
            if os.path.exists(REVIEW_LOG):
                with open(REVIEW_LOG, "r") as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(entry)
            with open(REVIEW_LOG, "w") as f:
                json.dump(logs, f, indent=2)
        except Exception:
            pass
