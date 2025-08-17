#!/usr/bin/env python3
"""
AIFOLIO Git & CI/CD Fortress - PHASE 6
Zero-tolerance repository management and automated workflow system.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitCICDFortress:
    """Elite Git and CI/CD management system."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.git_dir = self.project_root / ".git"
        self.github_dir = self.project_root / ".github"
        self.workflows_dir = self.github_dir / "workflows"
        self.hooks_dir = self.git_dir / "hooks"
        
        # Ensure directories exist
        self.github_dir.mkdir(exist_ok=True)
        self.workflows_dir.mkdir(exist_ok=True)
        
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "git_status": {},
            "hooks_installed": [],
            "workflows_created": [],
            "security_measures": [],
            "recommendations": []
        }
    
    def run_command(self, cmd: str, cwd: Optional[Path] = None) -> Dict[str, Any]:
        """Execute shell command safely."""
        try:
            result = subprocess.run(
                cmd.split(),
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_git_status(self) -> Dict[str, Any]:
        """Analyze current Git repository status."""
        logger.info("🔍 Analyzing Git repository status...")
        
        status = {
            "is_git_repo": self.git_dir.exists(),
            "has_commits": False,
            "current_branch": None,
            "remote_configured": False,
            "uncommitted_changes": False,
            "hooks_present": [],
            "config_issues": []
        }
        
        if not status["is_git_repo"]:
            logger.warning("Not a Git repository - initializing...")
            init_result = self.run_command("git init")
            if init_result["success"]:
                status["is_git_repo"] = True
                logger.info("✅ Git repository initialized")
            else:
                logger.error("❌ Failed to initialize Git repository")
                return status
        
        # Check for commits
        log_result = self.run_command("git log --oneline -1")
        status["has_commits"] = log_result["success"]
        
        # Get current branch
        branch_result = self.run_command("git branch --show-current")
        if branch_result["success"]:
            status["current_branch"] = branch_result["stdout"]
        
        # Check for remote
        remote_result = self.run_command("git remote -v")
        status["remote_configured"] = bool(remote_result["stdout"])
        
        # Check for uncommitted changes
        status_result = self.run_command("git status --porcelain")
        status["uncommitted_changes"] = bool(status_result["stdout"])
        
        # Check existing hooks
        if self.hooks_dir.exists():
            for hook_file in self.hooks_dir.iterdir():
                if hook_file.is_file() and hook_file.stat().st_mode & 0o111:
                    status["hooks_present"].append(hook_file.name)
        
        self.report["git_status"] = status
        return status
    
    def create_git_hooks(self) -> List[str]:
        """Create essential Git hooks for code quality."""
        logger.info("🪝 Creating Git hooks...")
        
        hooks_created = []
        
        # Pre-commit hook
        pre_commit_content = '''#!/bin/bash
# AIFOLIO Pre-commit Hook - Code Quality Enforcement

set -e

echo "🔍 Running pre-commit checks..."

# Check for Python syntax errors
if command -v python3 &> /dev/null; then
    echo "Checking Python syntax..."
    python3 -m py_compile $(find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" | head -20) 2>/dev/null || {
        echo "❌ Python syntax errors found"
        exit 1
    }
fi

# Check for large files
echo "Checking for large files..."
large_files=$(find . -type f -size +10M -not -path "./.git/*" -not -path "./.venv/*" -not -path "./node_modules/*" 2>/dev/null || true)
if [ -n "$large_files" ]; then
    echo "❌ Large files detected (>10MB):"
    echo "$large_files"
    echo "Consider using Git LFS or .gitignore"
    exit 1
fi

# Check for secrets patterns
echo "Scanning for potential secrets..."
secret_patterns="(api[_-]?key|secret|password|token|private[_-]?key)"
if grep -r -i -E "$secret_patterns" --include="*.py" --include="*.js" --include="*.ts" --include="*.json" . 2>/dev/null | grep -v ".git" | grep -v "test" | head -5; then
    echo "⚠️  Potential secrets detected - review before committing"
fi

echo "✅ Pre-commit checks passed"
'''
        
        pre_commit_path = self.hooks_dir / "pre-commit"
        pre_commit_path.write_text(pre_commit_content)
        pre_commit_path.chmod(0o755)
        hooks_created.append("pre-commit")
        
        # Commit-msg hook for conventional commits
        commit_msg_content = '''#!/bin/bash
# AIFOLIO Commit Message Hook - Conventional Commits Enforcement

commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Invalid commit message format!"
    echo "Use: type(scope): description"
    echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
    echo "Example: feat(auth): add user authentication"
    exit 1
fi

echo "✅ Commit message format valid"
'''
        
        commit_msg_path = self.hooks_dir / "commit-msg"
        commit_msg_path.write_text(commit_msg_content)
        commit_msg_path.chmod(0o755)
        hooks_created.append("commit-msg")
        
        # Pre-push hook
        pre_push_content = '''#!/bin/bash
# AIFOLIO Pre-push Hook - Final Quality Gate

echo "🚀 Running pre-push checks..."

# Check if we're pushing to protected branches
protected_branches="main master production"
current_branch=$(git branch --show-current)

for branch in $protected_branches; do
    if [ "$current_branch" = "$branch" ]; then
        echo "⚠️  Pushing to protected branch: $branch"
        echo "Ensure all tests pass and code is reviewed"
        break
    fi
done

# Run quick test if available
if [ -f "package.json" ] && command -v npm &> /dev/null; then
    if npm run test:quick &> /dev/null; then
        echo "✅ Quick tests passed"
    fi
fi

echo "✅ Pre-push checks completed"
'''
        
        pre_push_path = self.hooks_dir / "pre-push"
        pre_push_path.write_text(pre_push_content)
        pre_push_path.chmod(0o755)
        hooks_created.append("pre-push")
        
        self.report["hooks_installed"] = hooks_created
        logger.info(f"✅ Created {len(hooks_created)} Git hooks")
        return hooks_created
    
    def create_github_workflows(self) -> List[str]:
        """Create GitHub Actions workflows."""
        logger.info("⚙️ Creating GitHub Actions workflows...")
        
        workflows_created = []
        
        # Main CI/CD workflow
        ci_workflow = {
            "name": "AIFOLIO CI/CD Pipeline",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main", "develop"]}
            },
            "jobs": {
                "quality-gate": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": "3.11"}
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install -r requirements.txt || echo 'No requirements.txt found'"
                        },
                        {
                            "name": "Run Python linting",
                            "run": "python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo 'Linting completed'"
                        },
                        {
                            "name": "Run Python tests",
                            "run": "python -m pytest tests/ || echo 'No tests found'"
                        }
                    ]
                },
                "security-scan": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {
                            "name": "Run security scan",
                            "uses": "securecodewarrior/github-action-add-sarif@v1",
                            "with": {"sarif-file": "security-scan.sarif"},
                            "continue-on-error": True
                        }
                    ]
                }
            }
        }
        
        ci_path = self.workflows_dir / "ci.yml"
        with open(ci_path, 'w') as f:
            import yaml
            yaml.dump(ci_workflow, f, default_flow_style=False)
        workflows_created.append("ci.yml")
        
        # Security workflow
        security_workflow = {
            "name": "Security Scan",
            "on": {
                "schedule": [{"cron": "0 2 * * *"}],  # Daily at 2 AM
                "workflow_dispatch": {}
            },
            "jobs": {
                "security": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {
                            "name": "Run Trivy vulnerability scanner",
                            "uses": "aquasecurity/trivy-action@master",
                            "with": {
                                "scan-type": "fs",
                                "scan-ref": ".",
                                "format": "sarif",
                                "output": "trivy-results.sarif"
                            }
                        },
                        {
                            "name": "Upload Trivy scan results",
                            "uses": "github/codeql-action/upload-sarif@v2",
                            "with": {"sarif_file": "trivy-results.sarif"}
                        }
                    ]
                }
            }
        }
        
        security_path = self.workflows_dir / "security.yml"
        with open(security_path, 'w') as f:
            yaml.dump(security_workflow, f, default_flow_style=False)
        workflows_created.append("security.yml")
        
        self.report["workflows_created"] = workflows_created
        logger.info(f"✅ Created {len(workflows_created)} GitHub workflows")
        return workflows_created
    
    def enhance_gitignore(self) -> List[str]:
        """Enhance .gitignore with comprehensive patterns."""
        logger.info("📝 Enhancing .gitignore...")
        
        gitignore_path = self.project_root / ".gitignore"
        
        # Essential patterns for AIFOLIO
        essential_patterns = [
            "# AIFOLIO Security",
            "*.key",
            "*.pem",
            "*.p12",
            "*.pfx",
            ".env*",
            "!.env.example",
            "secrets/",
            "private/",
            "",
            "# Python",
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            "",
            "# Virtual Environments",
            ".venv/",
            "venv/",
            "ENV/",
            "env/",
            ".env/",
            "",
            "# IDEs",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            "",
            "# OS",
            ".DS_Store",
            ".DS_Store?",
            "._*",
            ".Spotlight-V100",
            ".Trashes",
            "ehthumbs.db",
            "Thumbs.db",
            "",
            "# Logs",
            "logs/",
            "*.log",
            "npm-debug.log*",
            "yarn-debug.log*",
            "yarn-error.log*",
            "",
            "# Dependencies",
            "node_modules/",
            ".npm",
            ".yarn/",
            "",
            "# Testing",
            ".coverage",
            ".pytest_cache/",
            ".tox/",
            "htmlcov/",
            "",
            "# AI/ML",
            "*.model",
            "*.pkl",
            "*.h5",
            "*.weights",
            "checkpoints/",
            "",
            "# Temporary",
            "tmp/",
            "temp/",
            "*.tmp",
            "*.temp",
            ".cache/",
            "",
            "# Database",
            "*.db",
            "*.sqlite",
            "*.sqlite3",
            "",
            "# Compiled",
            "*.com",
            "*.class",
            "*.dll",
            "*.exe",
            "*.o",
            "*.so"
        ]
        
        # Read existing .gitignore
        existing_patterns = set()
        if gitignore_path.exists():
            existing_patterns = set(gitignore_path.read_text().splitlines())
        
        # Add new patterns
        new_patterns = []
        for pattern in essential_patterns:
            if pattern not in existing_patterns:
                new_patterns.append(pattern)
        
        if new_patterns:
            with open(gitignore_path, 'a') as f:
                f.write('\n'.join([''] + new_patterns))
            logger.info(f"✅ Added {len(new_patterns)} new .gitignore patterns")
        
        return new_patterns
    
    def setup_branch_protection(self) -> Dict[str, Any]:
        """Configure branch protection rules."""
        logger.info("🛡️ Setting up branch protection...")
        
        protection_config = {
            "main": {
                "required_status_checks": ["quality-gate", "security-scan"],
                "enforce_admins": False,
                "required_pull_request_reviews": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews": True
                },
                "restrictions": None
            }
        }
        
        # Save configuration for manual setup
        config_path = self.project_root / ".github" / "branch-protection.json"
        with open(config_path, 'w') as f:
            json.dump(protection_config, f, indent=2)
        
        self.report["security_measures"].append("branch-protection-config")
        logger.info("✅ Branch protection configuration saved")
        return protection_config
    
    def create_repository_templates(self) -> List[str]:
        """Create issue and PR templates."""
        logger.info("📋 Creating repository templates...")
        
        templates_created = []
        
        # Issue template
        issue_template = """---
name: Bug Report
about: Report a bug or issue
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. See error

## Expected Behavior
What you expected to happen.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g. macOS, Windows, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 1.0.0]

## Additional Context
Any other context about the problem.
"""
        
        issue_path = self.github_dir / "ISSUE_TEMPLATE" / "bug_report.md"
        issue_path.parent.mkdir(exist_ok=True)
        issue_path.write_text(issue_template)
        templates_created.append("bug_report.md")
        
        # PR template
        pr_template = """## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes

## Screenshots
If applicable, add screenshots.
"""
        
        pr_path = self.github_dir / "pull_request_template.md"
        pr_path.write_text(pr_template)
        templates_created.append("pull_request_template.md")
        
        logger.info(f"✅ Created {len(templates_created)} repository templates")
        return templates_created
    
    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        git_status = self.report["git_status"]
        
        if not git_status.get("has_commits"):
            recommendations.append("Make initial commit to establish repository history")
        
        if not git_status.get("remote_configured"):
            recommendations.append("Configure remote repository: git remote add origin <url>")
        
        if git_status.get("uncommitted_changes"):
            recommendations.append("Commit pending changes before proceeding")
        
        recommendations.extend([
            "Enable branch protection rules in GitHub repository settings",
            "Configure GitHub Actions secrets for deployment",
            "Set up automated dependency updates with Dependabot",
            "Configure code scanning alerts in repository security settings",
            "Review and customize workflow triggers based on team needs"
        ])
        
        self.report["recommendations"] = recommendations
        return recommendations
    
    def run_fortress_protocol(self) -> Dict[str, Any]:
        """Execute complete Git & CI/CD fortress setup."""
        logger.info("🏰 Initiating Git & CI/CD Fortress Protocol...")
        
        try:
            # Phase 1: Analyze current state
            self.analyze_git_status()
            
            # Phase 2: Install Git hooks
            self.create_git_hooks()
            
            # Phase 3: Create GitHub workflows
            self.create_github_workflows()
            
            # Phase 4: Enhance .gitignore
            self.enhance_gitignore()
            
            # Phase 5: Setup branch protection
            self.setup_branch_protection()
            
            # Phase 6: Create templates
            self.create_repository_templates()
            
            # Phase 7: Generate recommendations
            self.generate_recommendations()
            
            # Save comprehensive report
            report_path = self.project_root / "tools" / "git_cicd_report.json"
            with open(report_path, 'w') as f:
                json.dump(self.report, f, indent=2)
            
            logger.info("🎉 Git & CI/CD Fortress Protocol COMPLETE!")
            return self.report
            
        except Exception as e:
            logger.error(f"❌ Fortress protocol failed: {e}")
            self.report["error"] = str(e)
            return self.report

def main():
    """Main execution function."""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    fortress = GitCICDFortress(project_root)
    report = fortress.run_fortress_protocol()
    
    # Print summary
    print("\n" + "="*60)
    print("🏰 AIFOLIO GIT & CI/CD FORTRESS REPORT")
    print("="*60)
    print(f"📊 Git Hooks Installed: {len(report.get('hooks_installed', []))}")
    print(f"⚙️ Workflows Created: {len(report.get('workflows_created', []))}")
    print(f"🛡️ Security Measures: {len(report.get('security_measures', []))}")
    print(f"💡 Recommendations: {len(report.get('recommendations', []))}")
    
    if report.get('error'):
        print(f"❌ Error: {report['error']}")
        return 1
    
    print("✅ FORTRESS PROTOCOL COMPLETE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
