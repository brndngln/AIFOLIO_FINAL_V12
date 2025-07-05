import os
import json
from datetime import datetime

VIOLATIONS_PATH = os.path.join(
    os.path.dirname(__file__), "../../dashboard/legal_audit.json"
)
REVIEW_LOG = os.path.join(os.path.dirname(__file__), "../../logs/review_logs.json")


class LegalReview:
    @staticmethod
    def check_pdf(pdf_path):
        try:
            # Dummy: scan for required terms (replace with PDF parser in prod)
            required = ["copyright", "disclaimer", "terms"]
            violations = []
            with open(pdf_path, "rb") as f:
                content = f.read().decode(errors="ignore").lower()
                for term in required:
                    if term not in content:
                        violations.append(term)
            result = {
                "pdf": pdf_path,
                "violations": violations,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "FAIL" if violations else "PASS",
                "type": "legal",
            }
            LegalReview._log(result)
            LegalReview._sync_violations(result)
            return result
        except Exception as e:
            LegalReview._log(
                {
                    "pdf": pdf_path,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "WARN",
                    "type": "legal",
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

    @staticmethod
    def _sync_violations(entry):
        os.makedirs(os.path.dirname(VIOLATIONS_PATH), exist_ok=True)
        try:
            if os.path.exists(VIOLATIONS_PATH):
                with open(VIOLATIONS_PATH, "r") as f:
                    data = json.load(f)
            else:
                data = []
            data.append(entry)
            with open(VIOLATIONS_PATH, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
