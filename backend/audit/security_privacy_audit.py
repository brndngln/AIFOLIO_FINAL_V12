"""
AIFOLIO Security & Privacy Audit
Static, deterministic scan for secrets, hardcoded credentials, or privacy violations.
All secrets must be in .env and never checked into version control.
"""
import logging
import os

logger = logging.getLogger(__name__)

SECRET_PATTERNS = [
    "API_KEY",
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "WEBHOOK",
    "PRIVATE",
    "CREDENTIALS",
]

EXCLUDE_DIRS = [".git", "venv", "node_modules", "__pycache__"]


def scan_for_secrets(base_dir: str = ".") -> list:
    """Static, deterministic scan for secrets in codebase. Extension: real scanning pipeline."""
    logger.info(f"Scanning {base_dir} for secrets.")
    findings = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith((".py", ".js", ".yml", ".env")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for pattern in SECRET_PATTERNS:
                            if pattern in line and "os.getenv" not in line:
                                findings.append(
                                    {
                                        "file": path,
                                        "line": i,
                                        "pattern": pattern,
                                        "content": line.strip(),
                                    }
                                )
    logger.info(f"Secrets scan findings: {findings}")
    return findings
