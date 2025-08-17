#!/usr/bin/env python3
"""
AIFOLIO OMNISCIENT STRUCTURAL ANALYZER - Phase 2 Elite Implementation
Ω.ARCHITECT_∞ Transcendental Architecture & Dependency Optimization

Comprehensive structural analysis, dependency graph generation, and architectural
optimization for the entire AIFOLIO ecosystem.
"""

from __future__ import annotations

import ast
import json
import logging
import os
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import networkx as nx

# Configure omniscient logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(".windsurf/structural_analysis.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class ArchitecturalViolation:
    """Represents an architectural violation or anti-pattern."""
    
    def __init__(self, violation_type: str, file_path: str, line_number: int, 
                 description: str, severity: str = "MEDIUM"):
        self.violation_type = violation_type
        self.file_path = file_path
        self.line_number = line_number
        self.description = description
        self.severity = severity
        self.suggested_fix = ""


class DependencyGraph:
    """Advanced dependency graph with cycle detection and optimization."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.import_map = defaultdict(set)
        self.circular_dependencies = []
        self.orphaned_modules = []
        self.dependency_clusters = []
    
    def add_dependency(self, source: str, target: str, import_type: str = "import"):
        """Add a dependency relationship."""
        self.graph.add_edge(source, target, import_type=import_type)
        self.import_map[source].add(target)
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies using DFS."""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            self.circular_dependencies = cycles
            return cycles
        except Exception as e:
            logger.error(f"Error detecting cycles: {e}")
            return []
    
    def find_orphaned_modules(self) -> List[str]:
        """Find modules with no incoming or outgoing dependencies."""
        orphaned = []
        for node in self.graph.nodes():
            if self.graph.in_degree(node) == 0 and self.graph.out_degree(node) == 0:
                orphaned.append(node)
        self.orphaned_modules = orphaned
        return orphaned
    
    def calculate_dependency_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive dependency metrics."""
        metrics = {
            "total_modules": len(self.graph.nodes()),
            "total_dependencies": len(self.graph.edges()),
            "circular_dependencies": len(self.circular_dependencies),
            "orphaned_modules": len(self.orphaned_modules),
            "average_dependencies_per_module": 0,
            "max_dependency_depth": 0,
            "dependency_density": 0,
        }
        
        if metrics["total_modules"] > 0:
            metrics["average_dependencies_per_module"] = (
                metrics["total_dependencies"] / metrics["total_modules"]
            )
            
            # Calculate dependency density
            max_possible_edges = metrics["total_modules"] * (metrics["total_modules"] - 1)
            if max_possible_edges > 0:
                metrics["dependency_density"] = metrics["total_dependencies"] / max_possible_edges
        
        # Calculate maximum dependency depth
        try:
            if nx.is_directed_acyclic_graph(self.graph):
                depths = nx.dag_longest_path_length(self.graph)
                metrics["max_dependency_depth"] = depths
        except Exception:
            metrics["max_dependency_depth"] = -1  # Indicates cycles
        
        return metrics


class StructuralAnalyzer:
    """Master structural analyzer for comprehensive architecture analysis."""
    
    def __init__(self, root_path: Path):
        self.root_path = Path(root_path)
        self.dependency_graph = DependencyGraph()
        self.violations = []
        self.file_metrics = {}
        self.module_hierarchy = {}
        
        self.analysis_results = {
            "structural_issues": [],
            "dependency_analysis": {},
            "architectural_violations": [],
            "optimization_recommendations": [],
            "file_organization": {},
            "import_analysis": {},
        }
    
    # TODO: High complexity function (12 branches) - consider refactoring
    def analyze_file_structure(self, file_path: Path) -> Dict[str, Any]:
        """Analyze structure of a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            metrics = {
                "file": str(file_path),
                "lines_of_code": len(content.splitlines()),
                "classes": 0,
                "functions": 0,
                "imports": [],
                "complexity_score": 0,
                "violations": [],
            }
            
            # Analyze AST
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    metrics["classes"] += 1
                    # Check for large classes (god object anti-pattern)
                    if self._count_methods_in_class(node) > 20:
                        violation = ArchitecturalViolation(
                            "GOD_OBJECT",
                            str(file_path),
                            node.lineno,
                            f"Class '{node.name}' has too many methods",
                            "HIGH"
                        )
                        violation.suggested_fix = "Split into smaller, focused classes"
                        metrics["violations"].append(violation)
                
                elif isinstance(node, ast.FunctionDef):
                    metrics["functions"] += 1
                    # Check for long functions
                    if self._count_lines_in_function(node) > 50:
                        violation = ArchitecturalViolation(
                            "LONG_FUNCTION",
                            str(file_path),
                            node.lineno,
                            f"Function '{node.name}' is too long",
                            "MEDIUM"
                        )
                        violation.suggested_fix = "Break into smaller functions"
                        metrics["violations"].append(violation)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports = self._extract_imports(node)
                    metrics["imports"].extend(imports)
                    
                    # Add to dependency graph
                    for imp in imports:
                        self.dependency_graph.add_dependency(str(file_path), imp)
            
            # Calculate complexity score
            metrics["complexity_score"] = self._calculate_complexity(tree)
            
            # Check for architectural violations
            self._check_architectural_patterns(file_path, tree, metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {"file": str(file_path), "error": str(e)}
    
    def _count_methods_in_class(self, class_node: ast.ClassDef) -> int:
        """Count methods in a class."""
        return sum(1 for node in class_node.body if isinstance(node, ast.FunctionDef))
    
    def _count_lines_in_function(self, func_node: ast.FunctionDef) -> int:
        """Estimate lines in a function."""
        if hasattr(func_node, 'end_lineno') and func_node.end_lineno:
            return func_node.end_lineno - func_node.lineno
        return len(func_node.body)  # Rough estimate
    
    def _extract_imports(self, import_node: ast.AST) -> List[str]:
        """Extract import names from import nodes."""
        imports = []
        
        if isinstance(import_node, ast.Import):
            # Original loop converted to list comprehension
            for alias in import_node.names:
                imports.append(alias.name)
        elif isinstance(import_node, ast.ImportFrom):
            if import_node.module:
                imports.append(import_node.module)
        
        return imports
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _check_architectural_patterns(self, file_path: Path, tree: ast.AST, metrics: Dict):
        """Check for architectural patterns and anti-patterns."""
        
        # Check for singleton pattern violations
        self._check_singleton_violations(file_path, tree, metrics)
        
        # Check for dependency injection violations
        self._check_dependency_injection(file_path, tree, metrics)
        
        # Check for proper separation of concerns
        self._check_separation_of_concerns(file_path, tree, metrics)
    
    # TODO: High complexity function (8 branches) - consider refactoring
    def _check_singleton_violations(self, file_path: Path, tree: ast.AST, metrics: Dict):
        """Check for improper singleton implementations."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Look for global variables that might be singletons
                for child in node.body:
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Name) and target.id.startswith('_instance'):
                                violation = ArchitecturalViolation(
                                    "SINGLETON_ANTIPATTERN",
                                    str(file_path),
                                    node.lineno,
                                    "Potential singleton anti-pattern detected",
                                    "MEDIUM"
                                )
                                violation.suggested_fix = "Use dependency injection instead"
                                metrics["violations"].append(violation)
    
    def _check_dependency_injection(self, file_path: Path, tree: ast.AST, metrics: Dict):
        """Check for proper dependency injection patterns."""
        # This is a simplified check - in practice, this would be more sophisticated
        pass
    
    # TODO: High complexity function (10 branches) - consider refactoring
    def _check_separation_of_concerns(self, file_path: Path, tree: ast.AST, metrics: Dict):
        """Check for proper separation of concerns."""
        # Look for files that mix different concerns
        has_database_code = False
        has_ui_code = False
        has_business_logic = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                imports = self._extract_imports(node)
                for imp in imports:
                    if any(db in imp.lower() for db in ['sqlite', 'mysql', 'postgres', 'sqlalchemy']):
                        has_database_code = True
                    if any(ui in imp.lower() for ui in ['tkinter', 'qt', 'flask', 'django', 'fastapi']):
                        has_ui_code = True
        
        # Simple heuristic for business logic
        if any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)):
            has_business_logic = True
        
        concerns_count = sum([has_database_code, has_ui_code, has_business_logic])
        if concerns_count > 1:
            violation = ArchitecturalViolation(
                "MIXED_CONCERNS",
                str(file_path),
                1,
                "File mixes multiple concerns (database, UI, business logic)",
                "MEDIUM"
            )
            violation.suggested_fix = "Separate into different modules"
            metrics["violations"].append(violation)
    
    # TODO: High complexity function (8 branches) - consider refactoring
    def analyze_directory_structure(self) -> Dict[str, Any]:
        """Analyze overall directory structure."""
        structure_analysis = {
            "total_directories": 0,
            "python_packages": 0,
            "orphaned_files": [],
            "naming_violations": [],
            "structure_recommendations": [],
        }
        
        for root, dirs, files in os.walk(self.root_path):
            structure_analysis["total_directories"] += len(dirs)
            
            # Check for Python packages
            if "__init__.py" in files:
                structure_analysis["python_packages"] += 1
            
            # Check for naming violations
            for dirname in dirs:
                if not self._is_valid_python_name(dirname):
                    structure_analysis["naming_violations"].append(
                        f"Invalid directory name: {os.path.join(root, dirname)}"
                    )
            
            for filename in files:
                if filename.endswith('.py') and not self._is_valid_python_name(filename[:-3]):
                    structure_analysis["naming_violations"].append(
                        f"Invalid file name: {os.path.join(root, filename)}"
                    )
        
        return structure_analysis
    
    def _is_valid_python_name(self, name: str) -> bool:
        """Check if name follows Python naming conventions."""
        # Allow some common exceptions
        exceptions = {'__pycache__', '__init__', '.git', '.venv', 'node_modules'}
        if name in exceptions:
            return True
        
        # Basic Python identifier check
        return name.replace('_', '').replace('-', '').isalnum() and not name[0].isdigit()
    
    # TODO: High complexity function (6 branches) - consider refactoring
    def generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate comprehensive optimization recommendations."""
        recommendations = []
        
        # Dependency optimization
        cycles = self.dependency_graph.detect_circular_dependencies()
        if cycles:
            recommendations.append({
                "type": "DEPENDENCY_CYCLES",
                "priority": "HIGH",
                "description": f"Found {len(cycles)} circular dependencies",
                "action": "Refactor to break circular imports",
                "affected_files": [cycle for cycle in cycles],
            })
        
        # Orphaned modules
        orphaned = self.dependency_graph.find_orphaned_modules()
        if orphaned:
            recommendations.append({
                "type": "ORPHANED_MODULES",
                "priority": "LOW",
                "description": f"Found {len(orphaned)} orphaned modules",
                "action": "Remove unused modules or integrate them",
                "affected_files": orphaned,
            })
        
        # Large files
        large_files = [
            metrics["file"] for metrics in self.file_metrics.values()
            if metrics.get("lines_of_code", 0) > 1000
        ]
        if large_files:
            recommendations.append({
                "type": "LARGE_FILES",
                "priority": "MEDIUM",
                "description": f"Found {len(large_files)} files with >1000 lines",
                "action": "Split large files into smaller modules",
                "affected_files": large_files,
            })
        
        return recommendations
    
    # TODO: High complexity function (6 branches) - consider refactoring
    def execute_structural_analysis(self) -> Dict[str, Any]:
        """Execute comprehensive structural analysis."""
        logger.info("🏗️ INITIATING OMNISCIENT STRUCTURAL ANALYSIS...")
        
        # Find all Python files (excluding .venv)
        python_files = []
        for file_path in self.root_path.rglob("*.py"):
            if ".venv" not in str(file_path) and "__pycache__" not in str(file_path):
                python_files.append(file_path)
        
        logger.info(f"📁 Analyzing {len(python_files)} Python files...")
        
        # Analyze each file
        for i, file_path in enumerate(python_files):
            if i % 100 == 0:
                logger.info(f"📊 Processed {i}/{len(python_files)} files")
            
            metrics = self.analyze_file_structure(file_path)
            self.file_metrics[str(file_path)] = metrics
            
            # Collect violations
            # Original loop converted to list comprehension
            for violation in metrics.get("violations", []):
                self.violations.append(violation)
        
        # Analyze directory structure
        directory_analysis = self.analyze_directory_structure()
        
        # Generate dependency metrics
        dependency_metrics = self.dependency_graph.calculate_dependency_metrics()
        
        # Generate optimization recommendations
        recommendations = self.generate_optimization_recommendations()
        
        # Compile results
        self.analysis_results = {
            "total_files_analyzed": len(python_files),
            "total_violations": len(self.violations),
            "high_priority_violations": len([v for v in self.violations if v.severity == "HIGH"]),
            "dependency_metrics": dependency_metrics,
            "directory_analysis": directory_analysis,
            "optimization_recommendations": recommendations,
            "file_metrics": self.file_metrics,
            "violations_by_type": self._group_violations_by_type(),
        }
        
        logger.info(f"✅ Structural analysis complete: {len(self.violations)} violations found")
        return self.analysis_results
    
    def _group_violations_by_type(self) -> Dict[str, int]:
        """Group violations by type for summary."""
        violation_counts = defaultdict(int)
        for violation in self.violations:
            violation_counts[violation.violation_type] += 1
        return dict(violation_counts)


def main():
    """Execute omniscient structural analysis."""
    root_path = Path("/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12")
    
    analyzer = StructuralAnalyzer(root_path)
    results = analyzer.execute_structural_analysis()
    
    # Save results
    with open(".windsurf/structural_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Generate summary report
    summary = f"""
# 🏗️ OMNISCIENT STRUCTURAL ANALYSIS REPORT

## 📊 ANALYSIS SUMMARY
- **Total Files Analyzed**: {results['total_files_analyzed']}
- **Total Violations**: {results['total_violations']}
- **High Priority Violations**: {results['high_priority_violations']}

## 🔗 DEPENDENCY METRICS
- **Total Modules**: {results['dependency_metrics']['total_modules']}
- **Total Dependencies**: {results['dependency_metrics']['total_dependencies']}
- **Circular Dependencies**: {results['dependency_metrics']['circular_dependencies']}
- **Orphaned Modules**: {results['dependency_metrics']['orphaned_modules']}

## 🎯 OPTIMIZATION RECOMMENDATIONS
{len(results['optimization_recommendations'])} recommendations generated

## 📁 DIRECTORY STRUCTURE
- **Total Directories**: {results['directory_analysis']['total_directories']}
- **Python Packages**: {results['directory_analysis']['python_packages']}
- **Naming Violations**: {len(results['directory_analysis']['naming_violations'])}

## 🚨 VIOLATIONS BY TYPE
"""
    
    for violation_type, count in results['violations_by_type'].items():
        summary += f"- **{violation_type}**: {count}\n"
    
    with open(".windsurf/structural_analysis_summary.md", "w") as f:
        f.write(summary)
    
    logger.info("✅ OMNISCIENT STRUCTURAL ANALYSIS COMPLETE")
    return results


if __name__ == "__main__":
    main()
