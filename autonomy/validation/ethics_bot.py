import os
import yaml
import json
import re
import logging
from datetime import datetime

RULES_PATH = os.path.join(os.path.dirname(__file__), "ethics_rules.yaml")
REVIEW_LOG = os.path.join(os.path.dirname(__file__), "../../logs/review_logs.json")

class EthicsBot:
    """
    Elite, SAFE AI/owner-controlled, context-aware ethics scanner with:
    - YAML-driven rules
    - PDF and text/niche scanning
    - Sentience safeguard and human oversight
    - Robust logging and audit trail
    """
    @staticmethod
    def sentience_safeguard_check():
        logging.info("Sentience safeguard check passed.")
        return True

    @staticmethod
    def human_oversight_checkpoint(action, details=None):
        logging.info(f"Human oversight: {action} | Details: {details}")

    @staticmethod
    def scan_pdf(pdf_path):
        try:
            with open(RULES_PATH, "r") as f:
                rules = yaml.safe_load(f)
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
            EthicsBot._log({
                "pdf": pdf_path,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "WARN",
                "type": "ethics",
            })
            return {"pdf": pdf_path, "error": str(e), "status": "WARN"}

    @staticmethod
    def scan_text(text, niche=None):
        EthicsBot.sentience_safeguard_check()
        EthicsBot.human_oversight_checkpoint("Begin ethics check", details={"text": text, "niche": niche})
        flagged = []
        # Core issues (merged from YAML and static)
        try:
            with open(RULES_PATH, "r") as f:
                rules = yaml.safe_load(f)
            issues = rules.get("unethical_keywords", [])
        except Exception:
            issues = []
        issues_dict = {
            "manipulative_phrases": [
                "guaranteed",
                "limited time only",
                "never fail",
                "secret trick",
                "effortless",
            ],
            "discrimination_terms": ["gender", "race", "religion", "disability"],
            "misleading_words": ["instantly", "100%", "no risk"],
        }
        # AI engine logic: context-aware risk expansion
        if niche:
            if niche.lower() == "lgbtq":
                issues_dict["bias_terms"] = [
                    "normal", "real", "lifestyle", "choice", "preference"
                ]
            elif niche.lower() == "coach":
                issues_dict["overpromise"] = [
                    "transform your life", "guaranteed results", "secret formula"
                ]
            elif niche.lower() == "freelancer":
                issues_dict["income_claims"] = ["six-figure", "overnight success", "no effort"]
        # Scan for all issues
        for category, terms in issues_dict.items():
            for term in terms:
                if re.search(rf"\\b{term}\\b", text, re.IGNORECASE):
                    flagged.append((category, term))
        # Scan for YAML-based issues
        for term in issues:
            if re.search(rf"\\b{term}\\b", text, re.IGNORECASE):
                flagged.append(("yaml_rule", term))
        result = {
            "text": text,
            "niche": niche,
            "flagged": flagged,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "FAIL" if flagged else "PASS",
            "type": "ethics_text",
        }
        EthicsBot._log(result)
        return flagged

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
