import json
from pathlib import Path

GAP_PATH = Path(__file__).parent.parent / "logs" / "compliance_gaps.json"
RECOMMEND_PATH = (
    Path(__file__).parent.parent / "logs" / "remediation_recommendations.json"
)

REMEDIATION_LIBRARY = {
    "A.9.2.4": "Implement secret rotation policy and enforce strong authentication.",
    "A.9.4.2": "Enforce secure log-on procedures and MFA for overrides.",
    "A.12.4.1": "Enable detailed event logging and anomaly detection.",
    "A.18.2.2": "Establish periodic compliance reviews and workflow automation.",
    "AC-2": "Automate account management and review access regularly.",
    "IA-2": "Require multi-factor authentication for all privileged actions.",
    "AU-6": "Enable audit log analysis and alerting for suspicious events.",
    "PL-2": "Document and review system protection policies.",
}


def recommend_remediation():
    if not GAP_PATH.exists():
        return []
    with open(GAP_PATH, "r") as f:
        gaps = json.load(f)
    recommendations = []
    for g in gaps:
        rec = REMEDIATION_LIBRARY.get(
            g["control"], "Consult compliance experts for remediation guidance."
        )
        recommendations.append(
            {"standard": g["standard"], "control": g["control"], "recommendation": rec}
        )
    with open(RECOMMEND_PATH, "w") as f:
        json.dump(recommendations, f, indent=2)
    return recommendations
