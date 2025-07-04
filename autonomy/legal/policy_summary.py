<<<<<<< HEAD
import markdown
=======
>>>>>>> omni_repair_backup_20250704_1335
import re
from typing import Optional

POLICY_PATHS = {
    "terms_of_service": "terms_of_service.md",
    "refund_policy": "refund_policy.md",
    "privacy_policy": "privacy_policy.md"
}

def generate_policy_summary(policy_name: str, reading_level: str = "grade 8") -> Optional[str]:
    """
    Converts a legal policy document into a plain language summary.
    """
    import os
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, POLICY_PATHS.get(policy_name, ""))
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        text = f.read()
    # Remove markdown formatting for simplicity
    plain = re.sub(r'#.*\n', '', text)
    plain = re.sub(r'\*\*([^\*]+)\*\*', r'\1', plain)
    # Truncate or simplify to target reading level (static, not static)
    summary = plain.strip().replace('\n', ' ')
    # Limit to 500 chars for brevity
    return summary[:500] + ("..." if len(summary) > 500 else "")
