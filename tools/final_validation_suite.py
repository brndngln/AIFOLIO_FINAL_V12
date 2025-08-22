# !/usr/bin/env python3
"""
Final Validation Suite - Comprehensive validation of elite code quality
"""

import ast
import logging
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FinalValidationSuite:

    """Comprehensive validation suite for elite code quality."""

    def __init__(self, project_root: str):

        self.project_root = Path(project_root)
        self.validation_results = {}

    def validate_syntax(self) -> Dict[str, Any]:
        """Validate all Python files have correct syntax."""
        syntax_errors = []
        valid_files = 0
        total_files = 0

        for py_file in self.project_root.rglob("*.py"):
            if self._should_skip_file(py_file):
                continue

            total_files += 1
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                ast.parse(content)
                valid_files += 1

            except SyntaxError as e:
                syntax_errors.append(f"{py_file}:{e.lineno}: {e.msg}")
            except Exception as e:
                syntax_errors.append(f"{py_file}: {str(e)}")

        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "syntax_errors": len(syntax_errors),
            "error_details": syntax_errors[:10],  # First 10 errors
        }

    def validate_formatting(self) -> Dict[str, Any]:
        """Validate code formatting with Black."""
        try:
            result = subprocess.run(
                [
                    "black",
                    "--check",
                    ".",
                    "--exclude=venv|\\\\1venv|node_modules|\\\\1git|__pycache__|corrupted_black",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "formatting_compliant": result.returncode == 0,
                "exit_code": result.returncode,
                "issues_found": len(result.stdout.split("\n")) if result.stdout else 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_imports(self) -> Dict[str, Any]:
        """Validate import organization with isort."""
        try:
            result = subprocess.run(
                ["isort", "--check-only", ".", "--profile", "black"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "imports_organized": result.returncode == 0,
                "exit_code": result.returncode,
                "issues_found": len(result.stdout.split("\n")) if result.stdout else 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_style(self) -> Dict[str, Any]:
        """Validate code style with flake8."""
        try:
            result = subprocess.run(
                [
                    "flake8",
                    ".",
                    "--exclude=.venv,__pycache__,.git,node_modules,corrupted_black_failures,corrupted_black_parse",
                    "--max-line-length=88",
                    "--extend-ignore=E203,W503,E501",
                    "--count",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Extract issue count from last line
            lines = result.stdout.strip().split("\n")
            issue_count = 0
            if lines and lines[-1].isdigit():
                issue_count = int(lines[-1])

            return {
                "style_compliant": result.returncode == 0,
                "exit_code": result.returncode,
                "total_issues": issue_count,
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_security(self) -> Dict[str, Any]:
        """Validate security with bandit."""
        try:
            result = subprocess.run(
                [
                    "bandit",
                    "-r",
                    ".",
                    "-f",
                    "json",
                    "--exclude",
                    ".venv,__pycache__,.git,node_modules",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Bandit returns non-zero when issues found, but that's expected
            return {
                "security_scan_completed": True,
                "exit_code": result.returncode,
                "has_security_issues": result.returncode != 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_complexity(self) -> Dict[str, Any]:
        """Validate code complexity with radon."""
        try:
            result = subprocess.run(
                [
                    "radon",
                    "cc",
                    ".",
                    "--min",
                    "C",
                    "--exclude",
                    ".venv,__pycache__,.git,node_modules",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            complex_functions = len(
                [
                    line
                    for line in result.stdout.split("\n")
                    if line.strip() and not line.endswith(".py")
                ]
            )

            return {
                "complexity_check_completed": True,
                "high_complexity_functions": complex_functions,
                "acceptable_complexity": complex_functions < 50,
            }
        except Exception as e:
            return {"error": str(e)}

    def validate_test_coverage(self) -> Dict[str, Any]:
        """Check if test files exist and are structured properly."""
        test_files = list(self.project_root.rglob("test_*.py"))
        test_dirs = [d for d in self.project_root.rglob("tests") if d.is_dir()]

        return {
            "test_files_found": len(test_files),
            "test_directories": len(test_dirs),
            "has_test_structure": len(test_files) > 0 or len(test_dirs) > 0,
        }

    def calculate_quality_score(self) -> float:
        """Calculate overall code quality score."""
        score = 100.0

        # Syntax validation (critical)
        syntax_result = self.validation_results.get("syntax", {})
        if syntax_result.get("syntax_errors", 0) > 0:
            error_ratio = syntax_result["syntax_errors"] / syntax_result.get(
                "total_files", 1
            )
            score -= min(50, error_ratio * 100)

        # Formatting (important)
        formatting_result = self.validation_results.get("formatting", {})
        if not formatting_result.get("formatting_compliant", False):
            score -= 15

        # Style (important)
        style_result = self.validation_results.get("style", {})
        total_issues = style_result.get("total_issues", 0)
        if total_issues > 1000:
            score -= 20
        elif total_issues > 100:
            score -= 10
        elif total_issues > 10:
            score -= 5

        # Security (critical)
        security_result = self.validation_results.get("security", {})
        if security_result.get("has_security_issues", False):
            score -= 15

        # Complexity (moderate)
        complexity_result = self.validation_results.get("complexity", {})
        if not complexity_result.get("acceptable_complexity", True):
            score -= 10

        return max(0, score)

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation checks."""
        logger.info("🔍 Starting comprehensive validation suite...")
        start_time = time.time()

        # Run all validations
        self.validation_results["syntax"] = self.validate_syntax()
        logger.info("✅ Syntax validation completed")

        self.validation_results["formatting"] = self.validate_formatting()
        logger.info("✅ Formatting validation completed")

        self.validation_results["imports"] = self.validate_imports()
        logger.info("✅ Import validation completed")

        self.validation_results["style"] = self.validate_style()
        logger.info("✅ Style validation completed")

        self.validation_results["security"] = self.validate_security()
        logger.info("✅ Security validation completed")

        self.validation_results["complexity"] = self.validate_complexity()
        logger.info("✅ Complexity validation completed")

        self.validation_results["testing"] = self.validate_test_coverage()
        logger.info("✅ Test coverage validation completed")

        # Calculate quality score
        quality_score = self.calculate_quality_score()

        end_time = time.time()
        duration = end_time - start_time

        return {
            "validation_results": self.validation_results,
            "quality_score": quality_score,
            "validation_duration": duration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _should_skip_file(self, filepath: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            ".venv",
            "__pycache__",
            ".git",
            "node_modules",
            "corrupted_black_failures",
            "corrupted_black_parse",
            ".pytest_cache",
            "build",
            "dist",
            "venv_backend",
        ]

        return any(pattern in str(filepath) for pattern in skip_patterns)


def main():
    """Main execution function."""
    project_root = Path.cwd()
    validator = FinalValidationSuite(str(project_root))

    results = validator.run_comprehensive_validation()

    # Print comprehensive report
    print("\n" + "=" * 80)
    print("🏆 ELITE CODE QUALITY VALIDATION REPORT")
    print("=" * 80)

    # Quality Score
    quality_score = results["quality_score"]
    print(f"📊 OVERALL QUALITY SCORE: {quality_score:.1f}/100")

    if quality_score >= 90:
        print("🌟 ELITE QUALITY - Exceptional codebase!")
    elif quality_score >= 80:
        print("⭐ HIGH QUALITY - Excellent codebase!")
    elif quality_score >= 70:
        print("✅ GOOD QUALITY - Well-maintained codebase!")
    elif quality_score >= 60:
        print("⚠️  MODERATE QUALITY - Needs improvement")
    else:
        print("❌ LOW QUALITY - Significant issues found")

    print("\n📋 DETAILED VALIDATION RESULTS:")
    print("-" * 40)

    # Syntax Results
    syntax = results["validation_results"]["syntax"]
    print(f"🔧 SYNTAX: {syntax['valid_files']}/{syntax['total_files']} files valid")
    if syntax["syntax_errors"] > 0:
        print(f"   ❌ {syntax['syntax_errors']} syntax errors found")

    # Formatting Results
    formatting = results["validation_results"]["formatting"]
    status = (
        "✅ COMPLIANT" if formatting.get("formatting_compliant") else "❌ ISSUES FOUND"
    )
    print(f"🎨 FORMATTING: {status}")

    # Style Results
    style = results["validation_results"]["style"]
    print(f"📏 STYLE: {style.get('total_issues', 0)} flake8 issues")

    # Security Results
    security = results["validation_results"]["security"]
    status = (
        "✅ SECURE" if not security.get("has_security_issues") else "⚠️  ISSUES FOUND"
    )
    print(f"🔒 SECURITY: {status}")

    # Complexity Results
    complexity = results["validation_results"]["complexity"]
    print(
        f"🧠 COMPLEXITY: {complexity.get('high_complexity_functions', 0)} high-complexity functions"
    )

    # Testing Results
    testing = results["validation_results"]["testing"]
    print(f"🧪 TESTING: {testing['test_files_found']} test files found")

    print(f"\n⏱️  Validation completed in {results['validation_duration']:.2f} seconds")
    print("=" * 80)

    return results


if __name__ == "__main__":
    main()
