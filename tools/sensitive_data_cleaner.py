#!/usr/bin/env python3
"""
AIFOLIO Sensitive Data Cleaner
Systematically removes all sensitive information from the codebase
"""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Set


class SensitiveDataCleaner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.backup_dir = self.root_path / ".sensitive_backup"
        self.report_file = self.root_path / "sensitive_cleanup_report.json"

        # Patterns to find and replace
        self.sensitive_patterns = {
            # API Keys and Tokens
            r"Bearer\s+[A-Za-z0-9\-_\.]+": "Bearer YOUR_TOKEN_HERE",
            r'api[_-]?key["\s]*[:=]["\s]*[A-Za-z0-9\-_\.]+': 'api_key: "YOUR_API_KEY_HERE""',
            r'token["\s]*[:=]["\s]*[A-Za-z0-9\-_\.]+': 'token: "YOUR_TOKEN_HERE""',
            r'secret["\s]*[:=]["\s]*[A-Za-z0-9\-_\.]+': 'secret: "YOUR_SECRET_HERE""',
            r'password["\s]*[:=]["\s]*[A-Za-z0-9\-_\.]+': 'password: "YOUR_PASSWORD_HERE""',
            # Hardcoded credentials
            r"YOUR_BIOMETRIC_HERE": "YOUR_BIOMETRIC_HERE",
            r"YOUR_SECRET_HERE": "YOUR_SECRET_HERE",
            r"YOUR_LOCATION_HERE": "YOUR_LOCATION_HERE",
            r"YOUR_TIME_HERE": "YOUR_TIME_HERE",
            r"YOUR_FACE_3D_HERE": "YOUR_FACE_3D_HERE",
            r"YOUR_BEHAVIOR_HERE": "YOUR_BEHAVIOR_HERE",
            r"YOUR_PHASE9_KEY_HERE": "YOUR_PHASE9_KEY_HERE",
            # URLs with localhost and ports
            r"http://localhost:\d+": "http://localhost:PORT",
            r"https://localhost:\d+": "https://localhost:PORT",
            r"127\.0\.0\.1:\d+": "127.0.0.1:PORT",
            # JWT secrets
            r'JWT_SECRET["\s]*[:=]["\s]*[A-Za-z0-9\-_\.]+': 'JWT_SECRET=YOUR_JWT_SECRET_HERE"',
            # Database URLs
            r"redis://localhost:\d+": "redis://localhost:PORT",
            r'postgresql://user:pass@host:port/db"\']+': "postgresql://user:pass@host:port/db",
            r'mongodb://user:pass@host:port/db"\']+': "mongodb://user:pass@host:port/db",
            # Email addresses (basic pattern)
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}": "user@example.com",
        }

        # File extensions to process
        self.target_extensions = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".json",
            ".md",
            ".yml",
            ".yaml",
            ".sh",
            ".env",
            ".conf",
            ".config",
            ".txt",
            ".html",
            ".css",
        }

        # Directories to skip
        self.skip_dirs = {
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "venv_backend",
            ".windsurf",
            "dist",
            "build",
            ".ruff_cache",
        }

        self.cleaned_files = []
        self.skipped_files = []
        self.errors = []

    def create_backup(self, file_path: Path):
        """Create backup of original file"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)

        relative_path = file_path.relative_to(self.root_path)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            self.errors.append(f"Failed to backup {file_path}: {e}")
            return False

    def clean_file_content(self, content: str, file_path: Path) -> tuple[str, int]:
        """Clean sensitive data from file content"""
        original_content = content
        replacements = 0

        for pattern, replacement in self.sensitive_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                replacements += len(matches)

        return content, replacements

    def should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        # Skip if in excluded directory
        for part in file_path.parts:
            if part in self.skip_dirs:
                return False

        # Skip if not target extension
        if file_path.suffix not in self.target_extensions:
            return False

        # Skip backup files
        if ".backup" in file_path.name or ".bak" in file_path.name:
            return False

        return True

    def process_file(self, file_path: Path):
        """Process a single file"""
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Clean content
            cleaned_content, replacements = self.clean_file_content(content, file_path)

            if replacements > 0:
                # Create backup
                if self.create_backup(file_path):
                    # Write cleaned content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_content)

                    self.cleaned_files.append(
                        {
                            "file": str(file_path.relative_to(self.root_path)),
                            "replacements": replacements,
                        }
                    )
                    print(
                        f"✅ Cleaned {file_path.relative_to(self.root_path)} ({replacements} replacements)"
                    )
                else:
                    self.skipped_files.append(
                        str(file_path.relative_to(self.root_path))
                    )

        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            print(f"❌ Error processing {file_path.relative_to(self.root_path)}: {e}")

    def scan_and_clean(self):
        """Scan entire codebase and clean sensitive data"""
        print(f"🔍 Scanning {self.root_path} for sensitive data...")

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file() and self.should_process_file(file_path):
                self.process_file(file_path)

    def generate_report(self):
        """Generate cleanup report"""
        report = {
            "timestamp": str(Path().cwd()),
            "root_path": str(self.root_path),
            "summary": {
                "files_cleaned": len(self.cleaned_files),
                "files_skipped": len(self.skipped_files),
                "errors": len(self.errors),
            },
            "cleaned_files": self.cleaned_files,
            "skipped_files": self.skipped_files,
            "errors": self.errors,
            "backup_location": str(self.backup_dir),
        }

        with open(self.report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Cleanup Report:")
        print(f"   Files cleaned: {len(self.cleaned_files)}")
        print(f"   Files skipped: {len(self.skipped_files)}")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Report saved: {self.report_file}")
        print(f"   Backups saved: {self.backup_dir}")

    def update_gitignore(self):
        """Update .gitignore to prevent future sensitive data commits"""
        gitignore_path = self.root_path / ".gitignore"

        sensitive_patterns = [
            "# Sensitive Data Protection",
            "*.env",
            "*.env.local",
            "*.env.production",
            "*.env.staging",
            ".env.*",
            "config/secrets.json",
            "config/credentials.json",
            "**/secrets/**",
            "**/credentials/**",
            "**/*secret*",
            "**/*credential*",
            "**/*password*",
            "**/*token*",
            "**/*key*.json",
            "**/*key*.yml",
            "**/*key*.yaml",
            ".sensitive_backup/",
            "sensitive_cleanup_report.json",
            "",
            "# API Keys and Tokens",
            "**/api_keys/**",
            "**/tokens/**",
            "**/*.pem",
            "**/*.key",
            "**/*.crt",
            "**/*.p12",
            "**/*.pfx",
            "",
        ]

        try:
            # Read existing .gitignore
            existing_content = ""
            if gitignore_path.exists():
                with open(gitignore_path, "r") as f:
                    existing_content = f.read()

            # Add new patterns if not already present
            new_patterns = []
            for pattern in sensitive_patterns:
                if pattern not in existing_content:
                    new_patterns.append(pattern)

            if new_patterns:
                with open(gitignore_path, "a") as f:
                    f.write("\n".join(new_patterns) + "\n")
                print(f"✅ Updated .gitignore with {len(new_patterns)} new patterns")
            else:
                print("✅ .gitignore already contains sensitive data patterns")

        except Exception as e:
            self.errors.append(f"Failed to update .gitignore: {e}")
            print(f"❌ Failed to update .gitignore: {e}")


def main():
    """Main execution function"""
    root_path = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12"

    print("🧹 AIFOLIO Sensitive Data Cleaner")
    print("=" * 50)

    cleaner = SensitiveDataCleaner(root_path)

    # Scan and clean
    cleaner.scan_and_clean()

    # Update .gitignore
    cleaner.update_gitignore()

    # Generate report
    cleaner.generate_report()

    print("\n🎉 Sensitive data cleanup completed!")
    print("⚠️  Please review the backup files before deleting them.")
    print("📋 Check the cleanup report for details.")


if __name__ == "__main__":
    main()
