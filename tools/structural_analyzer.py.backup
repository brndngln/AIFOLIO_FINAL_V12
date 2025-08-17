#!/usr/bin/env python3
"""
AIFOLIO STRUCTURAL ANALYZER - Phase 2 Implementation
Ω.ARCHITECT_∞ Comprehensive Codebase Architecture Analysis

This module performs deep structural analysis, import resolution, dependency
auditing, and architectural harmonization across the entire AIFOLIO empire.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from stability_fortress import safe_file_operation, stability_wrapper

logger = logging.getLogger(__name__)


class StructuralAnalyzer:
    """Elite structural analysis engine for codebase architecture."""

    def __init__(self, root_path: Path):
        self.root_path = Path(root_path)
        self.analysis_results = {
            "files": {},
            "imports": defaultdict(set),
            "dependencies": defaultdict(set),
            "issues": [],
            "statistics": {},
            "recommendations": [],
        }
        self.python_files = []
        self.js_files = []
        self.config_files = []
        self.empty_files = []
        self.duplicate_files = []
        self.orphaned_files = []

    @stability_wrapper(timeout=300, max_retries=2)
    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive codebase analysis."""
        logger.info("🔍 Starting comprehensive structural analysis...")

        # Phase 1: File Discovery and Cataloging
        self._discover_files()

        # Phase 2: Import Analysis
        self._analyze_imports()

        # Phase 3: Dependency Mapping
        self._map_dependencies()

        # Phase 4: Issue Detection
        self._detect_issues()

        # Phase 5: Architecture Recommendations
        self._generate_recommendations()

        # Phase 6: Statistics Generation
        self._generate_statistics()

        logger.info("✅ Structural analysis completed")
        return self.analysis_results

    def _discover_files(self):
        """Discover and categorize all files in the codebase."""
        logger.info("📁 Discovering files...")

        ignore_patterns = {
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "dist",
            "build",
            "*.pyc",
            "*.pyo",
            ".DS_Store",
            "Thumbs.db",
            "*.log",
            "*.tmp",
        }

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore(
                file_path, ignore_patterns
            ):
                self._categorize_file(file_path)

        logger.info(
            f"📊 Discovered {len(self.python_files)} Python files, "
            f"{len(self.js_files)} JS files, {len(self.config_files)} config files"
        )

    def _should_ignore(self, file_path: Path, ignore_patterns: Set[str]) -> bool:
        """Check if file should be ignored based on patterns."""
        path_str = str(file_path)
        for pattern in ignore_patterns:
            if pattern in path_str or file_path.name.startswith("."):
                return True
        return False

    def _categorize_file(self, file_path: Path):
        """Categorize file by type and analyze basic properties."""
        relative_path = file_path.relative_to(self.root_path)
        file_info = {
            "path": str(relative_path),
            "size": file_path.stat().st_size,
            "type": self._get_file_type(file_path),
            "empty": file_path.stat().st_size == 0,
            "readable": os.access(file_path, os.R_OK),
            "writable": os.access(file_path, os.W_OK),
        }

        self.analysis_results["files"][str(relative_path)] = file_info

        # Categorize by type
        if file_path.suffix == ".py":
            self.python_files.append(file_path)
            if file_info["empty"]:
                self.empty_files.append(file_path)
        elif file_path.suffix in {".js", ".jsx", ".ts", ".tsx"}:
            self.js_files.append(file_path)
        elif file_path.suffix in {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}:
            self.config_files.append(file_path)

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type based on extension and content."""
        suffix = file_path.suffix.lower()
        type_mapping = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "react",
            ".ts": "typescript",
            ".tsx": "react-typescript",
            ".json": "json-config",
            ".yaml": "yaml-config",
            ".yml": "yaml-config",
            ".toml": "toml-config",
            ".md": "documentation",
            ".txt": "text",
            ".sh": "shell-script",
            ".sql": "database",
            ".html": "html",
            ".css": "stylesheet",
        }
        return type_mapping.get(suffix, "unknown")

    def _analyze_imports(self):
        """Analyze import statements and dependencies."""
        logger.info("🔗 Analyzing imports and dependencies...")

        for py_file in self.python_files:
            try:
                self._analyze_python_imports(py_file)
            except Exception as e:
                self.analysis_results["issues"].append(
                    {
                        "type": "import_analysis_error",
                        "file": str(py_file.relative_to(self.root_path)),
                        "error": str(e),
                    }
                )

    def _analyze_python_imports(self, file_path: Path):
        """Analyze Python imports in a specific file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST to extract imports
            tree = ast.parse(content)
            imports = self._extract_imports_from_ast(tree)

            relative_path = str(file_path.relative_to(self.root_path))
            self.analysis_results["imports"][relative_path] = imports

            # Check for problematic imports
            self._check_import_issues(file_path, imports)

        except SyntaxError as e:
            self.analysis_results["issues"].append(
                {
                    "type": "syntax_error",
                    "file": str(file_path.relative_to(self.root_path)),
                    "line": e.lineno,
                    "error": str(e),
                }
            )
        except Exception as e:
            logger.warning(f"Could not analyze imports in {file_path}: {e}")

    def _extract_imports_from_ast(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import information from AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno,
                        }
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(
                        {
                            "type": "from_import",
                            "module": module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "level": node.level,
                            "line": node.lineno,
                        }
                    )

        return imports

    def _check_import_issues(self, file_path: Path, imports: List[Dict[str, Any]]):
        """Check for import-related issues."""
        relative_path = str(file_path.relative_to(self.root_path))

        # Check for standard library shadowing
        stdlib_modules = {
            "os",
            "sys",
            "json",
            "time",
            "datetime",
            "collections",
            "itertools",
            "functools",
            "operator",
            "math",
            "random",
            "string",
            "threading",
            "multiprocessing",
            "subprocess",
            "urllib",
            "http",
            "email",
            "html",
            "xml",
            "csv",
            "sqlite3",
            "logging",
            "unittest",
            "asyncio",
            "concurrent",
        }

        file_stem = file_path.stem
        if file_stem in stdlib_modules:
            self.analysis_results["issues"].append(
                {
                    "type": "stdlib_shadowing",
                    "file": relative_path,
                    "module": file_stem,
                    "severity": "high",
                }
            )

        # Check for circular imports (simplified detection)
        for imp in imports:
            if imp["type"] == "from_import" and imp["level"] > 0:
                # Relative import - check if it could cause circular dependency
                self._check_circular_import(file_path, imp)

    def _check_circular_import(self, file_path: Path, import_info: Dict[str, Any]):
        """Check for potential circular import issues."""
        # This is a simplified check - a full implementation would build a dependency graph
        relative_path = str(file_path.relative_to(self.root_path))

        if import_info["level"] > 2:  # Deep relative imports are suspicious
            self.analysis_results["issues"].append(
                {
                    "type": "deep_relative_import",
                    "file": relative_path,
                    "import": import_info,
                    "severity": "medium",
                }
            )

    def _map_dependencies(self):
        """Map external dependencies and their usage."""
        logger.info("📦 Mapping dependencies...")

        # Find requirements files
        req_files = list(self.root_path.glob("*requirements*.txt"))
        req_files.extend(list(self.root_path.glob("pyproject.toml")))
        req_files.extend(list(self.root_path.glob("setup.py")))
        req_files.extend(list(self.root_path.glob("package.json")))

        for req_file in req_files:
            self._analyze_dependency_file(req_file)

    def _analyze_dependency_file(self, file_path: Path):
        """Analyze dependency file for external packages."""
        try:
            if file_path.name.endswith(".txt"):
                self._parse_requirements_txt(file_path)
            elif file_path.name == "pyproject.toml":
                self._parse_pyproject_toml(file_path)
            elif file_path.name == "package.json":
                self._parse_package_json(file_path)
        except Exception as e:
            logger.warning(f"Could not analyze dependency file {file_path}: {e}")

    def _parse_requirements_txt(self, file_path: Path):
        """Parse requirements.txt file."""
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith("#"):
                    # Parse package specification
                    package_spec = self._parse_package_spec(line)
                    if package_spec:
                        self.analysis_results["dependencies"]["python"].add(
                            (package_spec["name"], package_spec.get("version", "any"))
                        )

    def _parse_package_spec(self, spec: str) -> Optional[Dict[str, str]]:
        """Parse package specification like 'package>=1.0.0'."""
        # Simplified parsing - full implementation would handle all PEP 440 cases
        match = re.match(r"^([a-zA-Z0-9_-]+)([><=!]+)?(.+)?", spec.strip())
        if match:
            return {
                "name": match.group(1),
                "operator": match.group(2),
                "version": match.group(3),
            }
        return None

    def _parse_package_json(self, file_path: Path):
        """Parse package.json file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for dep_type in ["dependencies", "devDependencies"]:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        self.analysis_results["dependencies"]["javascript"].add(
                            (name, version)
                        )
        except json.JSONDecodeError as e:
            self.analysis_results["issues"].append(
                {
                    "type": "json_parse_error",
                    "file": str(file_path.relative_to(self.root_path)),
                    "error": str(e),
                }
            )

    def _detect_issues(self):
        """Detect various structural issues."""
        logger.info("🔍 Detecting structural issues...")

        # Detect empty files
        for file_path in self.empty_files:
            self.analysis_results["issues"].append(
                {
                    "type": "empty_file",
                    "file": str(file_path.relative_to(self.root_path)),
                    "severity": "low",
                }
            )

        # Detect potential duplicates (by name)
        self._detect_duplicate_files()

        # Detect orphaned files
        self._detect_orphaned_files()

        # Detect missing __init__.py files
        self._detect_missing_init_files()

    def _detect_duplicate_files(self):
        """Detect files with identical names in different directories."""
        name_to_paths = defaultdict(list)

        for py_file in self.python_files:
            name_to_paths[py_file.name].append(py_file)

        for name, paths in name_to_paths.items():
            if len(paths) > 1:
                self.analysis_results["issues"].append(
                    {
                        "type": "duplicate_filename",
                        "filename": name,
                        "paths": [str(p.relative_to(self.root_path)) for p in paths],
                        "severity": "medium",
                    }
                )

    def _detect_orphaned_files(self):
        """Detect files that are not imported by any other file."""
        imported_modules = set()

        # Collect all imported module names
        for file_imports in self.analysis_results["imports"].values():
            for imp in file_imports:
                if imp["type"] == "import":
                    imported_modules.add(imp["module"])
                elif imp["type"] == "from_import":
                    imported_modules.add(imp["module"])

        # Check which Python files are never imported
        for py_file in self.python_files:
            module_name = py_file.stem
            if module_name not in imported_modules and module_name != "__main__":
                # Check if it's a script (has if __name__ == "__main__")
                if not self._is_script_file(py_file):
                    self.analysis_results["issues"].append(
                        {
                            "type": "orphaned_file",
                            "file": str(py_file.relative_to(self.root_path)),
                            "severity": "low",
                        }
                    )

    def _is_script_file(self, file_path: Path) -> bool:
        """Check if file is a script (has main guard)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return 'if __name__ == "__main__"' in content
        except Exception:
            return False

    def _detect_missing_init_files(self):
        """Detect directories that should have __init__.py files."""
        python_dirs = set()

        # Find all directories containing Python files
        for py_file in self.python_files:
            python_dirs.add(py_file.parent)

        # Check for missing __init__.py files
        for py_dir in python_dirs:
            if py_dir != self.root_path:  # Skip root directory
                init_file = py_dir / "__init__.py"
                if not init_file.exists():
                    self.analysis_results["issues"].append(
                        {
                            "type": "missing_init_file",
                            "directory": str(py_dir.relative_to(self.root_path)),
                            "severity": "medium",
                        }
                    )

    def _generate_recommendations(self):
        """Generate architectural recommendations."""
        logger.info("💡 Generating recommendations...")

        recommendations = []

        # Recommend directory structure improvements
        if len(self.python_files) > 50:
            recommendations.append(
                {
                    "type": "structure",
                    "title": "Implement Modular Architecture",
                    "description": "Consider organizing code into modules: core/, ui/, features/, hooks/, config/, data/, lib/, types/, layouts/, assets/",
                    "priority": "high",
                }
            )

        # Recommend dependency management
        if not any(
            f.name in ["requirements.txt", "pyproject.toml"] for f in self.config_files
        ):
            recommendations.append(
                {
                    "type": "dependencies",
                    "title": "Add Dependency Management",
                    "description": "Create requirements.txt or pyproject.toml for Python dependencies",
                    "priority": "high",
                }
            )

        # Recommend fixing high-severity issues
        high_severity_issues = [
            i for i in self.analysis_results["issues"] if i.get("severity") == "high"
        ]
        if high_severity_issues:
            recommendations.append(
                {
                    "type": "fixes",
                    "title": "Fix High-Severity Issues",
                    "description": f"Address {len(high_severity_issues)} high-severity issues including stdlib shadowing",
                    "priority": "critical",
                }
            )

        self.analysis_results["recommendations"] = recommendations

    def _generate_statistics(self):
        """Generate comprehensive statistics."""
        stats = {
            "total_files": len(self.analysis_results["files"]),
            "python_files": len(self.python_files),
            "javascript_files": len(self.js_files),
            "config_files": len(self.config_files),
            "empty_files": len(self.empty_files),
            "total_issues": len(self.analysis_results["issues"]),
            "critical_issues": len(
                [
                    i
                    for i in self.analysis_results["issues"]
                    if i.get("severity") == "high"
                ]
            ),
            "total_size_bytes": sum(
                info["size"] for info in self.analysis_results["files"].values()
            ),
            "avg_file_size_bytes": sum(
                info["size"] for info in self.analysis_results["files"].values()
            )
            / max(1, len(self.analysis_results["files"])),
        }

        # Issue breakdown by type
        issue_types = defaultdict(int)
        for issue in self.analysis_results["issues"]:
            issue_types[issue["type"]] += 1

        stats["issue_breakdown"] = dict(issue_types)
        self.analysis_results["statistics"] = stats

    def save_analysis_report(self, output_path: Path):
        """Save comprehensive analysis report."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        logger.info(f"📊 Analysis report saved to {output_path}")


def main():
    """Main execution function."""
    root_path = Path("/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12")

    analyzer = StructuralAnalyzer(root_path)
    results = analyzer.analyze_codebase()

    # Save detailed report
    report_path = root_path / "tools" / "structural_analysis_report.json"
    analyzer.save_analysis_report(report_path)

    # Print summary
    stats = results["statistics"]
    print(f"\n🏗️ STRUCTURAL ANALYSIS COMPLETE")
    print(f"📁 Total Files: {stats['total_files']}")
    print(f"🐍 Python Files: {stats['python_files']}")
    print(f"⚠️  Total Issues: {stats['total_issues']}")
    print(f"🚨 Critical Issues: {stats['critical_issues']}")
    print(f"📊 Total Size: {stats['total_size_bytes'] / 1024 / 1024:.1f} MB")

    return results


if __name__ == "__main__":
    main()
