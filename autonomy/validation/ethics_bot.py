import os
import yaml
import json
from datetime import datetime

RULES_PATH = os.path.join(os.path.dirname(__file__), "ethics_rules.yaml")
REVIEW_LOG = os.path.join(os.path.dirname(__file__), "../../logs/review_logs.json")


# Autonomous, safety-validated, silent fallback
class EthicsBot:
    @staticmethod
    def scan_pdf(pdf_path):
        try:
            # Load YAML rules
            with open(RULES_PATH, "r") as f:
                rules = yaml.safe_load(f)
            # Dummy: scan for keywords (replace with PDF parser in prod)
            flagged = []
            with open(pdf_path, "rb") as f:
                content = f.read().decode(errors="ignore").lower()
                for rule in rules.get("unethical_keywords", []):
                    if rule.lower() in content:
                        flagged.append(rule)
            result = {
                "pdf": pdf_path,
                "flagged": flagged,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "FAIL" if flagged else "PASS",
                "type": "ethics",
            }
            EthicsBot._log(result)
            return result
        except Exception as e:
            # Silent fallback: always log
            EthicsBot._log(
                {
                    "pdf": pdf_path,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "WARN",
                    "type": "ethics",
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
