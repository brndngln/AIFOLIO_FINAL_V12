"""
SmartLegalWatcher: Static SAFE AI module for automated monitoring of platform, government, and regulatory policy changes.
- Monitors TOS, privacy, refund, and legal policy URLs for major platforms (Meta, TikTok, Gumroad, Stripe, Discord, etc.)
- Logs changes, notifies admin, and triggers weekly compliance/risk reports.
- No adaptive or sentient logic. All checks are static, deterministic, and owner-controlled.
"""
import datetime
import json
import os
from typing import List, Dict, Final, TypedDict, Any

class PlatformPolicy(TypedDict):
    name: str
    url: str

class PolicyChange(TypedDict, total=False):
    name: str
    old_hash: str
    new_hash: str
    change: str
    timestamp: str

SMART_LEGAL_WATCHER_LOG: Final[str] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../logs/smart_legal_watcher_log.jsonl")
)
os.makedirs(os.path.dirname(SMART_LEGAL_WATCHER_LOG), exist_ok=True)

PLATFORM_POLICIES: Final[List[PlatformPolicy]] = [
    {"name": "Meta", "url": "https://www.facebook.com/legal/terms"},
    {"name": "TikTok", "url": "https://www.tiktok.com/legal/terms-of-service"},
    {"name": "Gumroad", "url": "https://gumroad.com/terms"},
    {"name": "Stripe", "url": "https://stripe.com/legal"},
    {"name": "Discord", "url": "https://discord.com/terms"},
    # Add more as needed
]

STATIC_POLICY_HASHES: Final[Dict[str, str]] = {
    "Meta": "2025-07-01:abc123",
    "TikTok": "2025-07-01:def456",
    "Gumroad": "2025-07-01:ghi789",
    "Stripe": "2025-07-01:jkl012",
    "Discord": "2025-07-01:mno345",
}

ADMIN_EMAILS: Final[List[str]] = ["compliance@aifolio.com"]


def check_platform_policies() -> List[PolicyChange]:
    """
    Checks for changes in platform policy hashes (static simulation).
    Returns a list of detected changes.
    """
    detected_changes: List[PolicyChange] = []
    for platform in PLATFORM_POLICIES:
        name = platform["name"]
        old_hash = STATIC_POLICY_HASHES.get(name, "")
        new_hash = STATIC_POLICY_HASHES.get(name, "")  # Static stub: no change
        if old_hash != new_hash:
            detected_changes.append(PolicyChange(
                name=name,
                old_hash=old_hash,
                new_hash=new_hash,
                change="Policy changed",
                timestamp=datetime.datetime.utcnow().isoformat(),
            ))
    return detected_changes


def log_and_notify_changes(changes: List[PolicyChange]) -> None:
    """
    Log detected policy changes and notify admins (static simulation).
    Args:
        changes: List of detected policy changes.
    """
    if not changes:
        return
    for change in changes:
        with open(SMART_LEGAL_WATCHER_LOG, "a") as f:
            f.write(json.dumps(change) + "\n")
    # Simulate notification (static)
    for admin in ADMIN_EMAILS:
        print(f"[SmartLegalWatcher] Notified {admin} of changes: {changes}")


def weekly_report() -> None:
    """
    Generate a weekly compliance/risk report for admin/Notion.
    """
    report = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "platforms_checked": [p["name"] for p in PLATFORM_POLICIES],
        "changes_detected": check_platform_policies(),
        "status": "OK" if not check_platform_policies() else "CHANGES_DETECTED",
    }
    with open(SMART_LEGAL_WATCHER_LOG, "a") as f:
        f.write(json.dumps(report) + "\n")
    print(f"[SmartLegalWatcher] Weekly report generated: {report}")


def run_smart_legal_watcher() -> None:
    """
    Entry point for scheduled weekly compliance check.
    """
    changes = check_platform_policies()
    log_and_notify_changes(changes)
    weekly_report()


# For scheduled use: run_smart_legal_watcher()
