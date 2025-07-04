"""
Script to scan for hardcoded secrets and .env leaks in the codebase.
"""
import os
import re

SECRET_PATTERNS = [
    r"SECRET_KEY\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?",
    r"AIFOLIO_PASSWORD_HASH\s*=\s*['\"]?[A-Za-z0-9$./]{20,}['\"]?",
    r"api_key\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?",
    r"token\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?",
]

IGNORED_DIRS = {'.git', 'node_modules', 'build', 'dist', '__pycache__', '.venv'}

results = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
    for file in files:
        if file.endswith(('.py', '.js', '.ts', '.env', '.json')):
            with open(os.path.join(root, file), errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    for pat in SECRET_PATTERNS:
                        if re.search(pat, line):
                            results.append(f"{os.path.join(root, file)}:{i}: {line.strip()}")

if results:
    print("Potential secrets found:")
    for r in results:
        print(r)
else:
    print("No secrets found.")
