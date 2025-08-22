#!/usr/bin/env python3
"""
AIFOLIO_FINAL_V12 Structural & Dependency Purification System
Architectural Blueprint Reconception with Zero-Tolerance Optimization
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class StructuralPurifier:
    """Supreme architectural optimizer with dependency management"""

    def __init__(self, root_path: str, inventory_path: str):
        self.root_path = Path(root_path)
        self.inventory_path = Path(inventory_path)
        self.inventory = self._load_inventory()
        self.processed_files = 0
        self.fixes_applied = 0
        self.start_time = time.time()

        # Structural issues tracking
        self.structural_issues = {
            "circular_dependencies": [],
            "unused_imports": [],
            "duplicate_files": [],
            "orphaned_files": [],
            "misplaced_files": [],
            "import_conflicts": [],
            "dependency_violations": [],
        }

        # Directory structure optimization
        self.optimal_structure = {
            "core": ["aifolio.py", "config", "utils"],
            "api": ["endpoints", "middleware", "auth"],
            "ui": ["components", "layouts", "assets"],
            "data": ["models", "schemas", "migrations"],
            "services": ["external", "internal", "integrations"],
            "tests": ["unit", "integration", "e2e"],
            "docs": ["api", "user", "developer"],
            "scripts": ["deployment", "maintenance", "utilities"],
        }

    def _load_inventory(self) -> Dict[str, Any]:
        """Load the omniscient inventory"""
        try:
            with open(self.inventory_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load inventory: {e}")
            return {}

    def purify_structure(self):
        """Execute comprehensive structural purification"""
        print("🧱 PHASE 2: STRUCTURAL & DEPENDENCY PURIFICATION INITIATED")
        print("=" * 70)

        # Step 1: Analyze current structure
        self._analyze_directory_structure()

        # Step 2: Detect circular dependencies
        self._detect_circular_dependencies()

        # Step 3: Find unused imports
        self._find_unused_imports()

        # Step 4: Identify duplicate files
        self._identify_duplicate_files()

        # Step 5: Locate orphaned files
        self._locate_orphaned_files()

        # Step 6: Optimize import structure
        self._optimize_import_structure()

        # Step 7: Reorganize directory structure
        self._reorganize_directory_structure()

        # Step 8: Generate dependency graph
        self._generate_clean_dependency_graph()

        self._generate_structural_report()
        return self.structural_issues

    def _analyze_directory_structure(self):
        """Analyze current directory structure for optimization opportunities"""
        print("📂 Analyzing directory structure...")

        directories = self.inventory.get("directories", {})
        files = self.inventory.get("files", {})

        # Analyze directory depth and organization
        depth_analysis = defaultdict(list)
        for dir_path in directories.keys():
            depth = len(Path(dir_path).parts)
            depth_analysis[depth].append(dir_path)

        # Find deeply nested directories (potential reorganization candidates)
        for depth, dirs in depth_analysis.items():
            if depth > 5:  # More than 5 levels deep
                for dir_path in dirs:
                    self.structural_issues["misplaced_files"].append(
                        {
                            "path": dir_path,
                            "issue": "excessive_nesting",
                            "depth": depth,
                            "suggestion": "Consider flattening directory structure",
                        }
                    )

        # Analyze file distribution
        file_distribution = defaultdict(int)
        for file_path, file_info in files.items():
            parent_dir = str(Path(file_path).parent)
            file_distribution[parent_dir] += 1

        # Find directories with too many files
        for dir_path, file_count in file_distribution.items():
            if file_count > 50:  # More than 50 files in one directory
                self.structural_issues["misplaced_files"].append(
                    {
                        "path": dir_path,
                        "issue": "overcrowded_directory",
                        "file_count": file_count,
                        "suggestion": "Consider subdividing into logical subdirectories",
                    }
                )

    def _detect_circular_dependencies(self):
        """Detect circular dependencies in the codebase"""
        print("🔄 Detecting circular dependencies...")

        imports = self.inventory.get("imports", {})
        dependency_graph = defaultdict(set)

        # Build dependency graph
        for file_path, file_imports in imports.items():
            for imp in file_imports:
                # Map import to actual file
                for other_file in imports.keys():
                    if imp in str(other_file) or other_file.endswith(f"{imp}.py"):
                        dependency_graph[file_path].add(other_file)

        # Detect cycles using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(node, path):
            if node in rec_stack:
                # Found cycle - find where it starts
                try:
                    cycle_start = path.index(node)
                    cycle = path[cycle_start:] + [node]
                    return cycle
                except ValueError:
                    # Node not in path, create simple cycle
                    return [node, node]

            if node in visited:
                return None

            visited.add(node)
            rec_stack.add(node)

            for neighbor in dependency_graph.get(node, set()):
                cycle = has_cycle(neighbor, path + [node])
                if cycle:
                    return cycle

            rec_stack.remove(node)
            return None

        # Check for cycles
        for node in dependency_graph:
            if node not in visited:
                cycle = has_cycle(node, [])
                if cycle:
                    self.structural_issues["circular_dependencies"].append(
                        {
                            "cycle": cycle,
                            "severity": "high",
                            "suggestion": "Refactor to break circular dependency",
                        }
                    )

    def _find_unused_imports(self):
        """Find unused imports across the codebase"""
        print("📦 Finding unused imports...")

        files = self.inventory.get("files", {})

        for file_path, file_info in files.items():
            if file_info.get("category") != "python":
                continue

            try:
                full_path = self.root_path / file_path
                if not full_path.exists():
                    continue

                content = full_path.read_text(encoding="utf-8", errors="ignore")

                # Parse AST to find imports and usage
                try:
                    tree = ast.parse(content)
                    imports_found = []

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports_found.append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports_found.append(node.module)
                            for alias in node.names:
                                imports_found.append(alias.name)

                    # Check if imports are used
                    for imp in imports_found:
                        if (
                            imp not in content or content.count(imp) <= 1
                        ):  # Only appears in import
                            self.structural_issues["unused_imports"].append(
                                {
                                    "file": file_path,
                                    "import": imp,
                                    "suggestion": "Remove unused import",
                                }
                            )

                except SyntaxError:
                    continue

            except Exception as e:
                continue

    def _identify_duplicate_files(self):
        """Identify duplicate files by content hash"""
        print("🔍 Identifying duplicate files...")

        files = self.inventory.get("files", {})
        hash_groups = defaultdict(list)

        # Group files by hash
        for file_path, file_info in files.items():
            file_hash = file_info.get("hash")
            if file_hash and file_info.get("size_bytes", 0) > 100:  # Skip tiny files
                hash_groups[file_hash].append(file_path)

        # Find duplicates
        for file_hash, file_list in hash_groups.items():
            if len(file_list) > 1:
                # Determine which file to keep (prefer shorter path, main directories)
                primary_file = min(
                    file_list, key=lambda x: (len(x), "backup" in x, "temp" in x)
                )
                duplicates = [f for f in file_list if f != primary_file]

                self.structural_issues["duplicate_files"].append(
                    {
                        "primary": primary_file,
                        "duplicates": duplicates,
                        "hash": file_hash,
                        "suggestion": f"Remove {len(duplicates)} duplicate file(s)",
                    }
                )

    def _locate_orphaned_files(self):
        """Locate orphaned files with no references"""
        print("🏝️ Locating orphaned files...")

        files = self.inventory.get("files", {})
        imports = self.inventory.get("imports", {})

        # Build reference map
        referenced_files = set()
        for file_path, file_imports in imports.items():
            for imp in file_imports:
                for other_file in files.keys():
                    if imp in str(other_file):
                        referenced_files.add(other_file)

        # Find orphaned files
        for file_path, file_info in files.items():
            if file_info.get("category") == "python":
                if (
                    file_path not in referenced_files
                    and not file_path.endswith("__init__.py")
                    and not file_path.startswith("test")
                    and "main" not in file_path.lower()
                ):

                    self.structural_issues["orphaned_files"].append(
                        {
                            "file": file_path,
                            "suggestion": "Consider removing or integrating orphaned file",
                        }
                    )

    def _optimize_import_structure(self):
        """Optimize import structure and organization"""
        print("⚡ Optimizing import structure...")

        files = self.inventory.get("files", {})

        for file_path, file_info in files.items():
            if file_info.get("category") != "python":
                continue

            try:
                full_path = self.root_path / file_path
                if not full_path.exists():
                    continue

                content = full_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.split("\n")

                # Analyze import organization
                import_lines = []
                other_lines = []
                imports_started = False

                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped.startswith("import ") or stripped.startswith("from "):
                        import_lines.append((i, line))
                        imports_started = True
                    elif imports_started and stripped and not stripped.startswith("#"):
                        # Imports section ended
                        break
                    elif not imports_started:
                        other_lines.append(line)

                # Check for import organization issues
                if len(import_lines) > 1:
                    # Check if imports are sorted
                    import_texts = [line for _, line in import_lines]
                    sorted_imports = sorted(
                        import_texts,
                        key=lambda x: (
                            not x.startswith("from "),  # 'import' before 'from'
                            x.lower(),
                        ),
                    )

                    if import_texts != sorted_imports:
                        self.structural_issues["import_conflicts"].append(
                            {
                                "file": file_path,
                                "issue": "unsorted_imports",
                                "suggestion": "Sort imports alphabetically",
                            }
                        )

            except Exception as e:
                continue

    def _reorganize_directory_structure(self):
        """Reorganize directory structure for optimal architecture"""
        print("🏗️ Analyzing directory reorganization opportunities...")

        files = self.inventory.get("files", {})

        # Analyze current organization vs optimal structure
        current_structure = defaultdict(list)

        for file_path in files.keys():
            parts = Path(file_path).parts
            if len(parts) > 1:
                top_level = parts[0]
                current_structure[top_level].append(file_path)

        # Suggest reorganization based on file types and patterns
        reorganization_suggestions = []

        for top_level, file_list in current_structure.items():
            if top_level not in self.optimal_structure:
                # Analyze file patterns to suggest proper location
                python_files = [f for f in file_list if f.endswith(".py")]
                js_files = [
                    f for f in file_list if f.endswith((".js", ".jsx", ".ts", ".tsx"))
                ]
                config_files = [
                    f
                    for f in file_list
                    if f.endswith((".json", ".yaml", ".yml", ".toml"))
                ]

                if (
                    len(python_files) > len(js_files)
                    and "test" not in top_level.lower()
                ):
                    suggested_location = (
                        "core" if "api" not in top_level.lower() else "api"
                    )
                elif len(js_files) > 0:
                    suggested_location = "ui"
                elif len(config_files) > 0:
                    suggested_location = "config"
                else:
                    suggested_location = "misc"

                reorganization_suggestions.append(
                    {
                        "current": top_level,
                        "suggested": suggested_location,
                        "file_count": len(file_list),
                        "reasoning": f"Based on file types: {len(python_files)} Python, {len(js_files)} JS, {len(config_files)} Config",
                    }
                )

        if reorganization_suggestions:
            self.structural_issues["misplaced_files"].extend(reorganization_suggestions)

    def _generate_clean_dependency_graph(self):
        """Generate optimized dependency graph"""
        print("📊 Generating clean dependency graph...")

        imports = self.inventory.get("imports", {})
        clean_graph = {}

        for file_path, file_imports in imports.items():
            # Filter to only internal dependencies
            internal_deps = []
            for imp in file_imports:
                for other_file in imports.keys():
                    if imp in str(other_file) and other_file != file_path:
                        internal_deps.append(other_file)

            if internal_deps:
                clean_graph[file_path] = internal_deps

        # Save clean dependency graph
        graph_path = (
            self.root_path / ".windsurf" / "cleanup" / "clean_dependency_graph.json"
        )
        graph_path.parent.mkdir(parents=True, exist_ok=True)

        with open(graph_path, "w") as f:
            json.dump(clean_graph, f, indent=2)

        print(f"📊 Clean dependency graph saved to: {graph_path}")

    def _generate_structural_report(self):
        """Generate comprehensive structural purification report"""
        report_path = (
            self.root_path / ".windsurf" / "cleanup" / "structural_report.json"
        )
        report_path.parent.mkdir(parents=True, exist_ok=True)

        # Calculate metrics
        total_issues = sum(len(issues) for issues in self.structural_issues.values())

        report = {
            "summary": {
                "total_issues_found": total_issues,
                "processing_time": time.time() - self.start_time,
                "files_analyzed": len(self.inventory.get("files", {})),
            },
            "structural_issues": self.structural_issues,
            "optimization_recommendations": {
                "high_priority": [
                    "Resolve circular dependencies",
                    "Remove duplicate files",
                    "Clean unused imports",
                ],
                "medium_priority": [
                    "Reorganize deeply nested directories",
                    "Sort import statements",
                    "Address orphaned files",
                ],
                "low_priority": [
                    "Optimize directory structure",
                    "Standardize naming conventions",
                ],
            },
            "architectural_health": {
                "dependency_complexity": len(
                    self.structural_issues["circular_dependencies"]
                ),
                "code_duplication": len(self.structural_issues["duplicate_files"]),
                "import_cleanliness": len(self.structural_issues["unused_imports"]),
                "structural_organization": len(
                    self.structural_issues["misplaced_files"]
                ),
            },
            "timestamp": time.time(),
        }

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 STRUCTURAL PURIFICATION REPORT")
        print("=" * 50)
        print(f"🔍 Total Issues Found: {total_issues}")
        print(
            f"🔄 Circular Dependencies: {len(self.structural_issues['circular_dependencies'])}"
        )
        print(f"📦 Unused Imports: {len(self.structural_issues['unused_imports'])}")
        print(f"🔍 Duplicate Files: {len(self.structural_issues['duplicate_files'])}")
        print(f"🏝️ Orphaned Files: {len(self.structural_issues['orphaned_files'])}")
        print(f"📂 Misplaced Files: {len(self.structural_issues['misplaced_files'])}")
        print(f"⚡ Import Conflicts: {len(self.structural_issues['import_conflicts'])}")
        print(f"⏱️ Processing Time: {report['summary']['processing_time']:.2f} seconds")
        print(f"💾 Report saved to: {report_path}")


def main():
    """Execute structural purification with stability safeguards"""
    root_path = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12"
    inventory_path = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/.windsurf/cleanup/omniscient_inventory.json"

    print("🧱 AIFOLIO_FINAL_V12 STRUCTURAL PURIFICATION INITIATED")
    print("=" * 70)

    purifier = StructuralPurifier(root_path, inventory_path)
    structural_issues = purifier.purify_structure()

    print("\n🎯 PHASE 2 COMPLETE: STRUCTURAL & DEPENDENCY PURIFICATION")
    print("Architectural blueprint reconception executed successfully")

    return structural_issues


if __name__ == "__main__":
    main()
