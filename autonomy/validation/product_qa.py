import os
import json
from datetime import datetime

REVIEW_LOG = os.path.join(os.path.dirname(__file__), "../../logs/review_logs.json")


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
