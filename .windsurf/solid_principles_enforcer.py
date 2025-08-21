# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider monadic patterns for optional value handling
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
# Consider using dataclasses with frozen=True for immutability
# Consider using generators for memory efficiency
import functools
# Strategy pattern recommended to replace if/elif chains
# Builder pattern recommended for complex object construction
# Factory pattern applied for object creation
#!/usr/bin/env python3
"""
AIFOLIO SOLID PRINCIPLES ENFORCER - Phase 4.3 Implementation
Ω.ARCHITECT_∞ SOLID Principles Validation & Enforcement Engine

Analyzes and enforces SOLID principles across the entire codebase:
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import json
import logging
import sys

import ast

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
  handlers=[
  logging.FileHandler(".windsurf/solid_principles.log"),
  logging.StreamHandler(sys.stdout),
  ],
)
logger = logging.getLogger(__name__)

# Consider adding __slots__ for memory optimization
class SOLIDViolation:
  """Represents a SOLID principle violation."""

  def __init__(self, principle: str, file_path: str, line_number: int,
  class_name: str, description: str, severity: str = "MEDIUM"):
  self.principle = principle  # SRP, OCP, LSP, ISP, DIP
  self.file_path = file_path
  self.line_number = line_number
  self.class_name = class_name
  self.description = description
  self.severity = severity
  self.refactoring_suggestion = ""
  self.estimated_effort = "MEDIUM"

class SRPAnalyzer:
  """Single Responsibility Principle analyzer."""

  def analyze_class_responsibilities(self, class_node: ast.ClassDef, file_path: str) -> List[SOLIDViolation]:
  """Analyze if a class has multiple responsibilities."""
  violations = []

  # Count different types of methods
  method_types = {
  'data_access': 0,  # save, load, get, set, fetch
  'business_logic': 0,  # calculate, process, validate, compute
  'presentation': 0,  # format, display, render, show
  'utility': 0,  # helper, convert, transform
  'lifecycle': 0,  # init, setup, cleanup, destroy
  }

  for node in class_node.body:
  if isinstance(node, ast.FunctionDef):
  method_name = node.name.lower()

  # Categorize methods
  if any(keyword in method_name for keyword in ['save', 'load', 'get', 'set', 'fetch', 'store', 'retrieve']):
  method_types['data_access'] += 1
  elif any(keyword in method_name for keyword in ['calculate', 'process', 'validate', 'compute', 'analyze']):
  method_types['business_logic'] += 1
  elif any(keyword in method_name for keyword in ['format', 'display', 'render', 'show', 'print']):
  method_types['presentation'] += 1
  elif any(keyword in method_name for keyword in ['convert', 'transform', 'parse', 'serialize']):
  method_types['utility'] += 1
  elif any(keyword in method_name for keyword in ['init', 'setup', 'cleanup', 'destroy', 'close']):
  method_types['lifecycle'] += 1

  # Check for multiple responsibilities
  active_responsibilities = sum(1 for count in method_types.values() if count > 0)

  if active_responsibilities >= 3:
  violation = SOLIDViolation(
  "SRP",
  file_path,
  class_node.lineno,
  class_node.name,
  f"Class has {active_responsibilities} different responsibilities",
  "HIGH"
  )
  violation.refactoring_suggestion = "Split class into focused, single-responsibility classes"
  violation.estimated_effort = "HIGH"
  violations.append(violation)

  # Check for god classes (too many methods)
  total_methods = sum(1 for node in class_node.body if isinstance(node, ast.FunctionDef))
  if total_methods > 15:
  violation = SOLIDViolation(
  "SRP",
  file_path,
  class_node.lineno,
  class_node.name,
  f"God class with {total_methods} methods",
  "HIGH"
  )
  violation.refactoring_suggestion = "Break into smaller, focused classes"
  violation.estimated_effort = "HIGH"
  violations.append(violation)

  return violations

class OCPAnalyzer:
  """Open/Closed Principle analyzer."""

  def analyze_extensibility(self, class_node: ast.ClassDef, file_path: str) -> List[SOLIDViolation]:
  """Analyze if class is open for extension but closed for modification."""
  violations = []

  # Look for long if-elif chains that should use polymorphism
  for node in ast.walk(class_node):
  if isinstance(node, ast.If):
  elif_count = self._count_elif_chain(node)

  if elif_count >= 3:
  violation = SOLIDViolation(
  "OCP",
  file_path,
  node.lineno,
  class_node.name,
  f"Long if-elif chain ({elif_count} branches) violates OCP",
  "MEDIUM"
  )
  violation.refactoring_suggestion = "Use polymorphism or strategy pattern"
  violation.estimated_effort = "HIGH"
  violations.append(violation)

  # Check for hardcoded type checking
  for node in ast.walk(class_node):
  if isinstance(node, ast.Call):
  if (isinstance(node.func, ast.Name) and node.func.id == 'isinstance' or
  isinstance(node.func, ast.Name) and node.func.id == 'type'):
  violation = SOLIDViolation(
  "OCP",
  file_path,
  node.lineno,
  class_node.name,
  "Explicit type checking may violate OCP",
  "LOW"
  )
  violation.refactoring_suggestion = "Consider using polymorphism instead of type checking"
  violation.estimated_effort = "MEDIUM"
  violations.append(violation)

  return violations

  def _count_elif_chain(self, if_node: ast.If) -> int:
  """Count the length of an if-elif chain."""
  count = 1
  current = if_node

  while hasattr(current, 'orelse') and current.orelse:
  if isinstance(current.orelse[0], ast.If):
  count += 1
  current = current.orelse[0]
  else:
  break

  return count

class LSPAnalyzer:
  """Liskov Substitution Principle analyzer."""

  def analyze_inheritance(self, class_node: ast.ClassDef, file_path: str) -> List[SOLIDViolation]:
  """Analyze inheritance for LSP violations."""
  violations = []

  # Check if class has base classes
  if not class_node.bases:
  return violations

  # Look for method overrides that might violate LSP
  for node in class_node.body:
  if isinstance(node, ast.FunctionDef):
  # Check for methods that throw NotImplementedError
  for child in ast.walk(node):
  if (isinstance(child, ast.Raise) and
  isinstance(child.exc, ast.Call) and
  isinstance(child.exc.func, ast.Name) and
  child.exc.func.id == 'NotImplementedError'):

  violation = SOLIDViolation(
  "LSP",
  file_path,
  node.lineno,
  class_node.name,
  f"Method '{node.name}' raises NotImplementedError",
  "MEDIUM"
  )
  violation.refactoring_suggestion = "Provide proper implementation or redesign inheritance"
  violation.estimated_effort = "MEDIUM"
  violations.append(violation)

  # Check for methods that change expected behavior
  if node.name in ['__init__', '__new__'] and len(node.args.args) > 5:
  violation = SOLIDViolation(
  "LSP",
  file_path,
  node.lineno,
  class_node.name,
  f"Constructor with many parameters may violate LSP",
  "LOW"
  )
  violation.refactoring_suggestion = "Consider using builder pattern or dependency injection"
  violation.estimated_effort = "MEDIUM"
  violations.append(violation)

  return violations

class ISPAnalyzer:
  """Interface Segregation Principle analyzer."""

  def analyze_interfaces(self, class_node: ast.ClassDef, file_path: str) -> List[SOLIDViolation]:
  """Analyze for fat interfaces."""
  violations = []

  # Count public methods (interfaces)
  public_methods = []
  for node in class_node.body:
  if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
  public_methods.append(node.name)

  # Check for fat interfaces
  if len(public_methods) > 10:
  violation = SOLIDViolation(
  "ISP",
  file_path,
  class_node.lineno,
  class_node.name,
  f"Fat interface with {len(public_methods)} public methods",
  "MEDIUM"
  )
  violation.refactoring_suggestion = "Split into smaller, focused interfaces"
  violation.estimated_effort = "HIGH"
  violations.append(violation)

  # Look for unrelated method groups
  method_groups = self._categorize_methods(public_methods)
  if len(method_groups) > 2:
  violation = SOLIDViolation(
  "ISP",
  file_path,
  class_node.lineno,
  class_node.name,
  f"Interface has {len(method_groups)} unrelated method groups",
  "MEDIUM"
  )
  violation.refactoring_suggestion = "Segregate into focused interfaces"
  violation.estimated_effort = "HIGH"
  violations.append(violation)

  return violations

  def _categorize_methods(self, method_names: List[str]) -> Dict[str, List[str]]:
  """Categorize methods by their purpose."""
  categories = {
  'data': [],
  'business': [],
  'utility': [],
  'lifecycle': [],
  'other': []
  }

  for method in method_names:
  method_lower = method.lower()
  if any(keyword in method_lower for keyword in ['get', 'set', 'load', 'save', 'store']):
  categories['data'].append(method)
  elif any(keyword in method_lower for keyword in ['process', 'calculate', 'validate', 'compute']):
  categories['business'].append(method)
  elif any(keyword in method_lower for keyword in ['convert', 'format', 'transform']):
  categories['utility'].append(method)
  elif any(keyword in method_lower for keyword in ['init', 'setup', 'cleanup', 'close']):
  categories['lifecycle'].append(method)
  else:
  categories['other'].append(method)

  return {k: v for k, v in categories.items() if v}

class DIPAnalyzer:
  """Dependency Inversion Principle analyzer."""

  def analyze_dependencies(self, class_node: ast.ClassDef, file_path: str) -> List[SOLIDViolation]:
  """Analyze for dependency inversion violations."""
  violations = []

  # Look for direct instantiation of concrete classes
  for node in ast.walk(class_node):
  if isinstance(node, ast.Call):
  # Check for direct instantiation in __init__
  if (isinstance(node.func, ast.Name) and
  node.func.id[0].isupper()):  # Likely a class name

  # Find the method this call is in
  method_node = self._find_containing_method(class_node, node)
  if method_node and method_node.name == '__init__':
  violation = SOLIDViolation(
  "DIP",
  file_path,
  node.lineno,
  class_node.name,
  f"Direct instantiation of {node.func.id} in constructor",
  "MEDIUM"
  )
  violation.refactoring_suggestion = "Use dependency injection instead"
  violation.estimated_effort = "MEDIUM"
  violations.append(violation)

  # Check for imports of concrete implementations
  # This would require analyzing the full file, not just the class

  return violations

  def _find_containing_method(self, class_node: ast.ClassDef, target_node: ast.AST) -> Optional[ast.FunctionDef]:
  """Find the method that contains the target node."""
  for method in class_node.body:
  if isinstance(method, ast.FunctionDef):
  for node in ast.walk(method):
  if node is target_node:
  return method
  return None

class SOLIDPrinciplesEnforcer:
  """Master SOLID principles enforcer."""

  def __init__(self, root_path: Path):
  self.root_path = Path(root_path)
  self.srp_analyzer = SRPAnalyzer()
  self.ocp_analyzer = OCPAnalyzer()
  self.lsp_analyzer = LSPAnalyzer()
  self.isp_analyzer = ISPAnalyzer()
  self.dip_analyzer = DIPAnalyzer()

  self.violations = []
  self.solid_stats = {
  "files_analyzed": 0,
  "classes_analyzed": 0,
  "srp_violations": 0,
  "ocp_violations": 0,
  "lsp_violations": 0,
  "isp_violations": 0,
  "dip_violations": 0,
  "total_violations": 0,
  }

  def analyze_file_solid(self, file_path: Path) -> List[SOLIDViolation]:
  """Analyze a file for SOLID principle violations."""
  try:
  with open(file_path, 'r', encoding='utf-8') as f:
  content = f.read()

  tree = ast.parse(content)
  file_violations = []

  # Analyze each class in the file
  for node in ast.walk(tree):
  if isinstance(node, ast.ClassDef):
  self.solid_stats["classes_analyzed"] += 1

  # Analyze SRP
  srp_violations = self.srp_analyzer.analyze_class_responsibilities(node, str(file_path))
  file_violations.extend(srp_violations)
  self.solid_stats["srp_violations"] += len(srp_violations)

  # Analyze OCP
  ocp_violations = self.ocp_analyzer.analyze_extensibility(node, str(file_path))
  file_violations.extend(ocp_violations)
  self.solid_stats["ocp_violations"] += len(ocp_violations)

  # Analyze LSP
  lsp_violations = self.lsp_analyzer.analyze_inheritance(node, str(file_path))
  file_violations.extend(lsp_violations)
  self.solid_stats["lsp_violations"] += len(lsp_violations)

  # Analyze ISP
  isp_violations = self.isp_analyzer.analyze_interfaces(node, str(file_path))
  file_violations.extend(isp_violations)
  self.solid_stats["isp_violations"] += len(isp_violations)

  # Analyze DIP
  dip_violations = self.dip_analyzer.analyze_dependencies(node, str(file_path))
  file_violations.extend(dip_violations)
  self.solid_stats["dip_violations"] += len(dip_violations)

  return file_violations

  except Exception as e:
  logger.error(f"Error analyzing {file_path}: {e}")
  return []

  def execute_solid_analysis(self) -> Dict[str, Any]:
  """Execute comprehensive SOLID principles analysis."""
  logger.info("🏛️ INITIATING SOLID PRINCIPLES ANALYSIS...")

  # Find all Python files
  python_files = []
  for file_path in self.root_path.rglob("*.py"):
  if (".venv" not in str(file_path) and
  "__pycache__" not in str(file_path) and
  "test_" not in file_path.name):
  python_files.append(file_path)

  logger.info(f"🔍 Analyzing {len(python_files)} Python files for SOLID violations...")

  # Analyze files in batches
  batch_size = 100
  for i in range(0, len(python_files), batch_size):
  batch = python_files[i:i + batch_size]

  for file_path in batch:
  file_violations = self.analyze_file_solid(file_path)
  self.violations.extend(file_violations)
  self.solid_stats["files_analyzed"] += 1

  if i % 500 == 0:
  logger.info(f"📊 Analyzed {i}/{len(python_files)} files")

  self.solid_stats["total_violations"] = len(self.violations)

  # Generate SOLID compliance report
  compliance_report = self._generate_compliance_report()

  logger.info(f"🎯 SOLID analysis complete: {len(self.violations)} violations found")

  return {
  "solid_stats": self.solid_stats,
  "compliance_report": compliance_report,
  "violations": [
  {
  "principle": v.principle,
  "file": v.file_path,
  "line": v.line_number,
  "class": v.class_name,
  "description": v.description,
  "severity": v.severity,
  "suggestion": v.refactoring_suggestion,
  "effort": v.estimated_effort,
  }
  for v in self.violations
  ],
  }

  def _generate_compliance_report(self) -> Dict[str, Any]:
  """Generate SOLID compliance report."""
  total_classes = self.solid_stats["classes_analyzed"]
  if total_classes == 0:
  return {"compliance_score": 100, "grade": "A+"}

  # Calculate compliance scores
  srp_compliance = max(0, 100 - (self.solid_stats["srp_violations"] / total_classes * 100))
  ocp_compliance = max(0, 100 - (self.solid_stats["ocp_violations"] / total_classes * 100))
  lsp_compliance = max(0, 100 - (self.solid_stats["lsp_violations"] / total_classes * 100))
  isp_compliance = max(0, 100 - (self.solid_stats["isp_violations"] / total_classes * 100))
  dip_compliance = max(0, 100 - (self.solid_stats["dip_violations"] / total_classes * 100))

  overall_compliance = (srp_compliance + ocp_compliance + lsp_compliance +
  isp_compliance + dip_compliance) / 5

  # Assign grade
  if overall_compliance >= 95:
  grade = "A+"
  elif overall_compliance >= 90:
  grade = "A"
  elif overall_compliance >= 85:
  grade = "B+"
  elif overall_compliance >= 80:
  grade = "B"
  elif overall_compliance >= 75:
  grade = "C+"
  elif overall_compliance >= 70:
  grade = "C"
  elif overall_compliance >= 60:
  grade = "D"
  else:
  grade = "F"

  return {
  "compliance_score": round(overall_compliance, 2),
  "grade": grade,
  "principle_scores": {
  "SRP": round(srp_compliance, 2),
  "OCP": round(ocp_compliance, 2),
  "LSP": round(lsp_compliance, 2),
  "ISP": round(isp_compliance, 2),
  "DIP": round(dip_compliance, 2),
  },
  "recommendations": self._generate_solid_recommendations(),
  }

  def _generate_solid_recommendations(self) -> List[str]:
  """Generate SOLID improvement recommendations."""
  recommendations = []

  if self.solid_stats["srp_violations"] > 5:
  recommendations.append("Focus on breaking large classes into smaller, single-responsibility classes")

  if self.solid_stats["ocp_violations"] > 3:
  recommendations.append("Implement strategy pattern or polymorphism to reduce if-elif chains")

  if self.solid_stats["lsp_violations"] > 2:
  recommendations.append("Review inheritance hierarchies for proper substitutability")

  if self.solid_stats["isp_violations"] > 3:
  recommendations.append("Segregate fat interfaces into smaller, focused interfaces")

  if self.solid_stats["dip_violations"] > 5:
  recommendations.append("Implement dependency injection to reduce coupling")

  recommendations.append("Establish SOLID principles training for development team")
  recommendations.append("Add SOLID compliance checks to code review process")

  return recommendations

def main():
  """Execute SOLID principles analysis."""
  root_path = Path("/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12")

  enforcer = SOLIDPrinciplesEnforcer(root_path)
  results = enforcer.execute_solid_analysis()

  # Save results
  with open(".windsurf/solid_principles_results.json", "w") as f:
  json.dump(results, f, indent=2, default=str)

  # Generate summary report
  stats = results["solid_stats"]
  compliance = results["compliance_report"]

  summary = f"""
# 🏛️ SOLID PRINCIPLES COMPLIANCE REPORT

## 📊 ANALYSIS SUMMARY
- **Files Analyzed**: {stats['files_analyzed']}
- **Classes Analyzed**: {stats['classes_analyzed']}
- **Total Violations**: {stats['total_violations']}
- **Compliance Score**: {compliance['compliance_score']}%
- **Grade**: {compliance['grade']}

## 🎯 PRINCIPLE BREAKDOWN
- **SRP Violations**: {stats['srp_violations']} (Score: {compliance['principle_scores']['SRP']}%)
- **OCP Violations**: {stats['ocp_violations']} (Score: {compliance['principle_scores']['OCP']}%)
- **LSP Violations**: {stats['lsp_violations']} (Score: {compliance['principle_scores']['LSP']}%)
- **ISP Violations**: {stats['isp_violations']} (Score: {compliance['principle_scores']['ISP']}%)
- **DIP Violations**: {stats['dip_violations']} (Score: {compliance['principle_scores']['DIP']}%)

## 🔍 TOP VIOLATIONS
"""

  # Show top 10 violations
  high_severity_violations = [v for v in results["violations"] if v["severity"] == "HIGH"][:10]
  for violation in high_severity_violations:
  summary += f"- **{violation['principle']}** in `{Path(violation['file']).name}` (line {violation['line']}): {violation['description']}\n"

  summary += f"""
## 🎯 KEY RECOMMENDATIONS
"""

  for recommendation in compliance["recommendations"]:
  summary += f"- {recommendation}\n"

  summary += f"""
## 📋 IMPROVEMENT PLAN
1. **Phase 1**: Address all HIGH severity violations ({len(high_severity_violations)} items)
2. **Phase 2**: Implement design patterns for OCP violations
3. **Phase 3**: Refactor fat interfaces and god classes
4. **Phase 4**: Implement dependency injection framework
5. **Phase 5**: Establish SOLID compliance monitoring

## 🏆 SOLID EXCELLENCE TARGETS
- **Target Compliance Score**: 95%+
- **Target Grade**: A+
- **Maximum Violations per Principle**: < 5
- **Code Review Integration**: SOLID checks mandatory
"""

  with open(".windsurf/solid_principles_summary.md", "w") as f:
  f.write(summary)

  logger.info("✅ SOLID PRINCIPLES ANALYSIS COMPLETE")
  return results

if __name__ == "__main__":
  main()
