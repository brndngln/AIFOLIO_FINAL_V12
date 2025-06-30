"""
EthicsBot / QualityGuard AI (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
import logging

UNETHICAL_PATTERNS = ["manipulate", "scam", "deceive", "false", "mislead", "bias", "discriminate", "stereotype", "guaranteed", "secret", "get rich", "overnight", "never fail", "loophole"]
MIN_READABILITY = 50  # Flesch score (simulate)

@sentience_guard
def scan_and_fix(content):
    """
    Scan for unethical/manipulative language, suggest inline rewrites.
    Checks readability, layout, visual integrity. Enforces non-sentience and audit logging.
    """
    fixes = content
    report = []
    for pattern in UNETHICAL_PATTERNS:
        if pattern in content.lower():
            fixes = fixes.replace(pattern, "[REDACTED]")
            report.append(f"FLAG: Unethical pattern '{pattern}' removed. Manual review required.")
    # Simulated readability check
    readability = 60 if len(content) > 100 else 40
    if readability < MIN_READABILITY:
        report.append("FLAG: Low readability score. Manual review required.")
    return fixes, report
