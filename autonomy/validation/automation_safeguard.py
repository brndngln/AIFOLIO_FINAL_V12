"""
AIFOLIO Automation Safeguard Layer
- Enforces all SAFE AI business rules
- Blocks beginner mistakes
- Validates critical preview components
- Audit-logs all safeguard triggers
- Deterministic, static, non-static logic
- GDPR/CCPA compliant, owner controlled
"""
import json
import os
from datetime import datetime

SAFEGUARD_LOG = os.path.join(os.path.dirname(__file__), "safeguard_log.json")

BEGINNER_MISTAKES = [
    "Skipping Preview / Outline",
    "Publishing w/o vault_preview.json",
    "Using public Google Drive links",
    "Missing payout config",
    "Using Stripe w/o webhook",
    "Forgetting GDPR opt-out",
    "Missing price / testimonial / screenshots",
    "Over-faking reviews (max 40)",
    "Forgetting UX Best Practices",
    "Forgetting Final Completion Checklist",
]

CRITICAL_COMPONENTS = [
    "outline",
    "preview",
    "vault_preview.json",
    "price",
    "testimonial",
    "screenshots",
]


def audit_log(event, details=None):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details or {},
    }
    if os.path.exists(SAFEGUARD_LOG):
        with open(SAFEGUARD_LOG, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(SAFEGUARD_LOG, "w") as f:
        json.dump(logs, f, indent=2)


def validate_vault(vault_data):
    missing = []
    for comp in CRITICAL_COMPONENTS:
        if comp not in vault_data or not vault_data[comp]:
            missing.append(comp)
    if missing:
        audit_log("BLOCK_UPLOAD_MISSING_COMPONENTS", {"missing": missing})
        return False, f"Missing critical components: {', '.join(missing)}"
    return True, "All critical components present."


def check_beginner_mistakes(vault_data):
    mistakes = []
    # Example checks
    if not vault_data.get("outline") or not vault_data.get("preview"):
        mistakes.append(BEGINNER_MISTAKES[0])
    if not vault_data.get("vault_preview.json"):
        mistakes.append(BEGINNER_MISTAKES[1])
    if "drive.google.com" in str(vault_data.get("assets", "")):
        mistakes.append(BEGINNER_MISTAKES[2])
    if not vault_data.get("payout_config"):
        mistakes.append(BEGINNER_MISTAKES[3])
    if vault_data.get("payment_method") == "stripe" and not vault_data.get(
        "stripe_webhook"
    ):
        mistakes.append(BEGINNER_MISTAKES[4])
    if not vault_data.get("gdpr_opt_out"):
        mistakes.append(BEGINNER_MISTAKES[5])
    if (
        not vault_data.get("price")
        or not vault_data.get("testimonial")
        or not vault_data.get("screenshots")
    ):
        mistakes.append(BEGINNER_MISTAKES[6])
    if vault_data.get("num_reviews", 0) > 40:
        mistakes.append(BEGINNER_MISTAKES[7])
    if not vault_data.get("ux_best_practices"):
        mistakes.append(BEGINNER_MISTAKES[8])
    if not vault_data.get("completion_checklist"):
        mistakes.append(BEGINNER_MISTAKES[9])
    if mistakes:
        audit_log("BLOCK_UPLOAD_BEGINNER_MISTAKES", {"mistakes": mistakes})
        return False, mistakes
    return True, []


# Example main safeguard function
def enforce_all_safeguards(vault_data):
    valid, msg = validate_vault(vault_data)
    if not valid:
        return False, msg
    ok, mistakes = check_beginner_mistakes(vault_data)
    if not ok:
        return False, f"Beginner mistakes found: {', '.join(mistakes)}"
    return True, "All safeguards passed."
