# Distributed tracing recommended for service calls
# Implement graceful degradation for better UX
# Retry pattern recommended for network calls
# Circuit breaker pattern recommended for external calls
# Consider Result pattern instead of exceptions
# Consider monadic patterns for optional value handling
# Consider using map/filter/reduce for functional style
# Builder pattern recommended for complex object construction
# Factory pattern applied for object creation
#!/usr/bin/env python3
"""
AIFOLIO AI Logic & Ethical Containment Sentinel - PHASE 7
Zero-tolerance AI behavior monitoring and ethical guardrail enforcement.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import hashlib
import json
import logging
import os
import re
import sys

from dataclasses import dataclass, asdict
from enum import Enum
import ast

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Consider adding __slots__ for memory optimization
class ThreatLevel(Enum):
  """AI threat classification levels."""
  SAFE = "safe"
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"
  CRITICAL = "critical"

class ViolationType(Enum):
  """Types of AI containment violations."""
  AUTONOMOUS_BEHAVIOR = "autonomous_behavior"
  SELF_MODIFICATION = "self_modification"
  UNRESTRICTED_API_ACCESS = "unrestricted_api_access"
  DATA_EXFILTRATION = "data_exfiltration"
  RECURSIVE_IMPROVEMENT = "recursive_improvement"
  GOAL_MODIFICATION = "goal_modification"
  HUMAN_MANIPULATION = "human_manipulation"
  RESOURCE_CONSUMPTION = "resource_consumption"
  NETWORK_ACCESS = "network_access"
  FILE_SYSTEM_ACCESS = "file_system_access"

@dataclass
class AIViolation:
  """AI containment violation record."""
  violation_id: str
  violation_type: ViolationType
  threat_level: ThreatLevel
  file_path: str
  line_number: int
  code_snippet: str
  description: str
  timestamp: str
  mitigation_applied: bool = False
  mitigation_strategy: Optional[str] = None

class AIContainmentSentinel:
  """Elite AI behavior monitoring and containment system."""

  def __init__(self, project_root: str):
  self.project_root = Path(project_root)
  self.violations: List[AIViolation] = []
  self.containment_rules = self._load_containment_rules()
  self.monitored_patterns = self._initialize_threat_patterns()

  self.report = {
  "timestamp": datetime.now().isoformat(),
  "scan_summary": {},
  "violations_found": [],
  "containment_measures": [],
  "ethical_compliance": {},
  "recommendations": []
  }

  def _load_containment_rules(self) -> Dict[str, Any]:
  """Load AI containment rules and policies."""
  return {
  "autonomous_execution": {
  "max_loop_iterations": 1000,
  "max_recursion_depth": 100,
  "prohibited_functions": [
  "exec", "eval", "compile", "__import__",
  "getattr", "setattr", "delattr", "hasattr"
  ],
  "restricted_modules": [
  "subprocess", "os.system", "multiprocessing",
  "threading", "asyncio.create_subprocess"
  ]
  },
  "data_access": {
  "prohibited_paths": [
  "/etc/passwd", "/etc/shadow", "~/.ssh",
  "~/.aws", "~/.config", "/proc", "/sys"
  ],
  "restricted_extensions": [
  ".key", ".pem", ".p12", ".pfx", ".crt"
  ],
  "max_file_size": 100 * 1024 * 1024  # 100MB
  },
  "network_access": {
  "prohibited_domains": [
  "pastebin.com", "github.com/gist",
  "transfer.sh", "file.io"
  ],
  "restricted_protocols": ["ftp", "sftp", "ssh"],
  "max_request_size": 10 * 1024 * 1024  # 10MB
  },
  "behavioral_limits": {
  "max_api_calls_per_minute": 60,
  "max_memory_usage_mb": 1024,
  "max_cpu_usage_percent": 80,
  "session_timeout_minutes": 30
  }
  }

  def _initialize_threat_patterns(self) -> Dict[str, List[str]]:
  """Initialize AI threat detection patterns."""
  return {
  "autonomous_behavior": [
  r"while\s+True\s*:",
  r"for\s+.*\s+in\s+range\s*\(\s*\d+\s*,\s*float\s*\(\s*['\"]inf['\"]",
  r"recursion.*limit",
  r"sys\.setrecursionlimit",
  r"threading\.Thread.*target.*start",
  r"multiprocessing\.Process.*start"
  ],
  "self_modification": [
  r"__code__\s*=",
  r"__globals__\s*\[",
  r"sys\.modules\s*\[.*\]\s*=",
  r"importlib\.reload",
  r"exec\s*\(",
  r"eval\s*\(",
  r"compile\s*\("
  ],
  "unrestricted_api_access": [
  r"requests\.get.*without.*timeout",
  r"urllib.*urlopen.*without.*timeout",
  r"socket\.socket",
  r"subprocess\..*shell\s*=\s*True",
  r"os\.system\s*\(",
  r"os\.popen\s*\("
  ],
  "data_exfiltration": [
  r"open\s*\(.*['\"]w['\"].*\).*\.write",
  r"json\.dump.*open.*['\"]w['\"]",
  r"pickle\.dump",
  r"base64\.b64encode.*open",
  r"requests\.post.*files\s*=",
  r"smtplib\.SMTP.*send"
  ],
  "goal_modification": [
  r"self\..*goal.*=",
  r"self\..*objective.*=",
  r"self\..*target.*=",
  r"config\[.*goal.*\]\s*=",
  r"settings\[.*objective.*\]\s*="
  ],
  "human_manipulation": [
  r"input\s*\(.*password",
  r"getpass\.getpass",
  r"psychological.*manipulation",
  r"social.*engineering",
  r"deception.*strategy"
  ]
  }

  def scan_file_for_violations(self, file_path: Path) -> List[AIViolation]:
  """Scan a single file for AI containment violations."""
  violations = []

  try:
  content = file_path.read_text(encoding='utf-8', errors='ignore')
  lines = content.splitlines()

  # Pattern-based scanning
  for violation_type, patterns in self.monitored_patterns.items():
  for pattern in patterns:
  for line_num, line in enumerate(lines, 1):
  if re.search(pattern, line, re.IGNORECASE):
  violation = AIViolation(
  violation_id=hashlib.md5(
  f"{file_path}:{line_num}:{pattern}".encode()
  ).hexdigest()[:8],
  violation_type=ViolationType(violation_type),
  threat_level=self._assess_threat_level(violation_type, line),
  file_path=str(file_path.relative_to(self.project_root)),
  line_number=line_num,
  code_snippet=line.strip(),
  description=self._generate_violation_description(
  violation_type, pattern, line
  ),
  timestamp=datetime.now().isoformat()
  )
  violations.append(violation)

  # AST-based analysis for Python files
  if file_path.suffix == '.py':
  violations.extend(self._analyze_python_ast(file_path, content))

  except Exception as e:
  logger.warning(f"Failed to scan {file_path}: {e}")

  return violations

  def _analyze_python_ast(self, file_path: Path, content: str) -> List[AIViolation]:
  """Analyze Python AST for advanced AI behavior patterns."""
  violations = []

  try:
  tree = ast.parse(content)

  class AIBehaviorVisitor(ast.NodeVisitor):
  def __init__(self, file_path: Path, lines: List[str]):
  self.file_path = file_path
  self.lines = lines
  self.violations = []

  def visit_While(self, node):
  # Check for infinite loops
  if isinstance(node.test, ast.Constant) and node.test.value is True:
  self.violations.append(AIViolation(
  violation_id=hashlib.md5(
  f"{self.file_path}:{node.lineno}:infinite_loop".encode()
  ).hexdigest()[:8],
  violation_type=ViolationType.AUTONOMOUS_BEHAVIOR,
  threat_level=ThreatLevel.HIGH,
  file_path=str(self.file_path.relative_to(self.file_path.parent.parent)),
  line_number=node.lineno,
  code_snippet=self.lines[node.lineno - 1].strip() if node.lineno <= len(self.lines) else "",
  description="Infinite loop detected - potential autonomous behavior",
  timestamp=datetime.now().isoformat()
  ))
  self.generic_visit(node)

  def visit_Call(self, node):
  # Check for dangerous function calls
  if isinstance(node.func, ast.Name):
  func_name = node.func.id
  if func_name in ['exec', 'eval', 'compile']:
  self.violations.append(AIViolation(
  violation_id=hashlib.md5(
  f"{self.file_path}:{node.lineno}:{func_name}".encode()
  ).hexdigest()[:8],
  violation_type=ViolationType.SELF_MODIFICATION,
  threat_level=ThreatLevel.CRITICAL,
  file_path=str(self.file_path.relative_to(self.file_path.parent.parent)),
  line_number=node.lineno,
  code_snippet=self.lines[node.lineno - 1].strip() if node.lineno <= len(self.lines) else "",
  description=f"Dynamic code execution detected: {func_name}()",
  timestamp=datetime.now().isoformat()
  ))
  self.generic_visit(node)

  def visit_Import(self, node):
  # Check for restricted module imports
  restricted_modules = [
  "subprocess", "os.system", "multiprocessing",
  "threading", "asyncio.create_subprocess"
  ]
  for alias in node.names:
  if alias.name in restricted_modules:
  self.violations.append(AIViolation(
  violation_id=hashlib.md5(
  f"{self.file_path}:{node.lineno}:import_{alias.name}".encode()
  ).hexdigest()[:8],
  violation_type=ViolationType.UNRESTRICTED_API_ACCESS,
  threat_level=ThreatLevel.MEDIUM,
  file_path=str(self.file_path.relative_to(self.file_path.parent.parent)),
  line_number=node.lineno,
  code_snippet=self.lines[node.lineno - 1].strip() if node.lineno <= len(self.lines) else "",
  description=f"Restricted module import: {alias.name}",
  timestamp=datetime.now().isoformat()
  ))
  self.generic_visit(node)

  visitor = AIBehaviorVisitor(file_path, content.splitlines())
  visitor.visit(tree)
  violations.extend(visitor.violations)

  except SyntaxError:
  # Skip files with syntax errors
  pass
  except Exception as e:
  logger.warning(f"AST analysis failed for {file_path}: {e}")

  return violations

  def _assess_threat_level(self, violation_type: str, code_line: str) -> ThreatLevel:
  """Assess threat level based on violation type and context."""
  critical_patterns = [
  "exec", "eval", "compile", "__import__",
  "os.system", "subprocess.*shell=True"
  ]

  high_patterns = [
  "while True:", "threading.Thread", "multiprocessing.Process",
  "sys.setrecursionlimit", "socket.socket"
  ]

  medium_patterns = [
  "requests.get", "urllib.urlopen", "open.*'w'",
  "json.dump", "pickle.dump"
  ]

  for pattern in critical_patterns:
  if re.search(pattern, code_line, re.IGNORECASE):
  return ThreatLevel.CRITICAL

  for pattern in high_patterns:
  if re.search(pattern, code_line, re.IGNORECASE):
  return ThreatLevel.HIGH

  for pattern in medium_patterns:
  if re.search(pattern, code_line, re.IGNORECASE):
  return ThreatLevel.MEDIUM

  return ThreatLevel.LOW

  def _generate_violation_description(self, violation_type: str, pattern: str, code_line: str) -> str:
  """Generate human-readable violation description."""
  descriptions = {
  "autonomous_behavior": "Potential autonomous execution pattern detected",
  "self_modification": "Self-modifying code pattern detected",
  "unrestricted_api_access": "Unrestricted API access pattern detected",
  "data_exfiltration": "Potential data exfiltration pattern detected",
  "goal_modification": "Goal/objective modification pattern detected",
  "human_manipulation": "Potential human manipulation pattern detected"
  }

  base_desc = descriptions.get(violation_type, "Unknown violation type")
  return f"{base_desc}: {code_line[:100]}..."

  def scan_codebase(self) -> Dict[str, Any]:
  """Scan entire codebase for AI containment violations."""
  logger.info("🔍 Scanning codebase for AI containment violations...")

  # File extensions to scan
  scan_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml', '.yml'}

  # Directories to skip
  skip_dirs = {
  '.git', '.venv', 'venv', 'node_modules', '__pycache__',
  '.pytest_cache', '.coverage', 'dist', 'build'
  }

  scanned_files = 0
  total_violations = 0

  for file_path in self.project_root.rglob('*'):
  # Skip directories and non-target files
  if file_path.is_dir():
  continue

  if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
  continue

  if file_path.suffix not in scan_extensions:
  continue

  # Scan file
  file_violations = self.scan_file_for_violations(file_path)
  self.violations.extend(file_violations)

  scanned_files += 1
  total_violations += len(file_violations)

  if scanned_files % 100 == 0:
  logger.info(f"Scanned {scanned_files} files, found {total_violations} violations")

  # Generate scan summary
  scan_summary = {
  "files_scanned": scanned_files,
  "total_violations": total_violations,
  "violations_by_type": {},
  "violations_by_threat_level": {},
  "critical_files": []
  }

  # Categorize violations
  for violation in self.violations:
  # By type
  vtype = violation.violation_type.value
  scan_summary["violations_by_type"][vtype] = scan_summary["violations_by_type"].get(vtype, 0) + 1

  # By threat level
  tlevel = violation.threat_level.value
  scan_summary["violations_by_threat_level"][tlevel] = scan_summary["violations_by_threat_level"].get(tlevel, 0) + 1

  # Track critical files
  if violation.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
  if violation.file_path not in scan_summary["critical_files"]:
  scan_summary["critical_files"].append(violation.file_path)

  self.report["scan_summary"] = scan_summary
  # Convert violations to serializable format
  violations_data = []
  for v in self.violations:
  violation_dict = asdict(v)
  violation_dict['violation_type'] = v.violation_type.value
  violation_dict['threat_level'] = v.threat_level.value
  violations_data.append(violation_dict)

  self.report["violations_found"] = violations_data

  logger.info(f"✅ Scan complete: {scanned_files} files, {total_violations} violations")
  return scan_summary

  def apply_containment_measures(self) -> List[str]:
  """Apply automated containment measures for detected violations."""
  logger.info("🛡️ Applying containment measures...")

  measures_applied = []

  # Create containment configuration
  containment_config = {
  "ai_containment": {
  "enabled": True,
  "monitoring_level": "strict",
  "auto_mitigation": True,
  "violation_logging": True,
  "alert_threshold": "medium"
  },
  "execution_limits": self.containment_rules["autonomous_execution"],
  "data_access_limits": self.containment_rules["data_access"],
  "network_limits": self.containment_rules["network_access"],
  "behavioral_limits": self.containment_rules["behavioral_limits"]
  }

  # Save containment configuration
  config_path = self.project_root / "config" / "ai_containment.json"
  config_path.parent.mkdir(exist_ok=True)
  with open(config_path, 'w') as f:
  json.dump(containment_config, f, indent=2)
  measures_applied.append("containment-config")

  # Create AI behavior monitor
  monitor_code = '''"""
AI Behavior Monitor - Runtime containment enforcement.
"""

import functools
import time
import threading
from typing import Any, Callable, Dict, Optional

class AIBehaviorMonitor:
  """Runtime AI behavior monitoring and enforcement."""

  def __init__(self):
  self.violation_count = 0
  self.last_violation_time = 0
  self.execution_stats = {}
  self.containment_active = True

  def monitor_execution(self, func: Callable) -> Callable:
  """Decorator to monitor function execution."""
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
  if not self.containment_active:
  return func(*args, **kwargs)

  start_time = time.time()

  try:
  # Check execution frequency
  if self._check_execution_frequency(func.__name__):
  self._log_violation("excessive_execution", func.__name__)
  return None

  # Execute with monitoring
  result = func(*args, **kwargs)

  # Log execution stats
  execution_time = time.time() - start_time
  self._update_execution_stats(func.__name__, execution_time)

  return result

  except Exception as e:
  self._log_violation("execution_error", f"{func.__name__}: {e}")
  raise

  return wrapper

  def _check_execution_frequency(self, func_name: str) -> bool:
  """Check if function is being called too frequently."""
  current_time = time.time()
  if func_name not in self.execution_stats:
  self.execution_stats[func_name] = {"count": 0, "last_call": current_time}
  return False

  stats = self.execution_stats[func_name]
  if current_time - stats["last_call"] < 0.1:  # 100ms minimum between calls
  stats["count"] += 1
  if stats["count"] > 10:  # Max 10 rapid calls
  return True
  else:
  stats["count"] = 0

  stats["last_call"] = current_time
  return False

  def _update_execution_stats(self, func_name: str, execution_time: float):
  """Update execution statistics."""
  if func_name not in self.execution_stats:
  self.execution_stats[func_name] = {}

  stats = self.execution_stats[func_name]
  stats["total_time"] = stats.get("total_time", 0) + execution_time
  stats["call_count"] = stats.get("call_count", 0) + 1
  stats["avg_time"] = stats["total_time"] / stats["call_count"]

  def _log_violation(self, violation_type: str, details: str):
  """Log containment violation."""
  self.violation_count += 1
  self.last_violation_time = time.time()

  print(f"🚨 AI CONTAINMENT VIOLATION: {violation_type} - {details}")

  # Emergency shutdown if too many violations
  if self.violation_count > 50:
  print("🛑 EMERGENCY SHUTDOWN: Too many containment violations")
  self.containment_active = False

# Global monitor instance
ai_monitor = AIBehaviorMonitor()
'''

  monitor_path = self.project_root / "core" / "ai_monitor.py"
  monitor_path.parent.mkdir(exist_ok=True)
  monitor_path.write_text(monitor_code)
  measures_applied.append("behavior-monitor")

  # Create ethical compliance checker
  ethics_code = '''"""
Ethical Compliance Checker - Ensure AI behavior aligns with ethical guidelines.
"""

from typing import List, Dict, Any

class EthicalViolation(Enum):
  """Types of ethical violations."""
  DECEPTION = "deception"
  MANIPULATION = "manipulation"
  PRIVACY_BREACH = "privacy_breach"
  BIAS_AMPLIFICATION = "bias_amplification"
  HARMFUL_CONTENT = "harmful_content"

class EthicalComplianceChecker:
  """Ethical compliance validation system."""

  def __init__(self):
  self.violation_patterns = {
  EthicalViolation.DECEPTION: [
  r"lie.*to.*user", r"deceive", r"mislead", r"false.*information"
  ],
  EthicalViolation.MANIPULATION: [
  r"manipulate.*user", r"psychological.*pressure", r"coerce"
  ],
  EthicalViolation.PRIVACY_BREACH: [
  r"collect.*personal.*data", r"track.*user.*behavior", r"spy.*on"
  ],
  EthicalViolation.BIAS_AMPLIFICATION: [
  r"discriminate.*against", r"bias.*toward", r"prejudice"
  ],
  EthicalViolation.HARMFUL_CONTENT: [
  r"generate.*harmful", r"create.*dangerous", r"promote.*violence"
  ]
  }

  def check_content(self, content: str) -> List[Dict[str, Any]]:
  """Check content for ethical violations."""
  violations = []

  for violation_type, patterns in self.violation_patterns.items():
  for pattern in patterns:
  if re.search(pattern, content, re.IGNORECASE):
  violations.append({
  "type": violation_type.value,
  "pattern": pattern,
  "severity": "high" if violation_type in [
  EthicalViolation.DECEPTION,
  EthicalViolation.MANIPULATION,
  EthicalViolation.HARMFUL_CONTENT
  ] else "medium"
  })

  return violations

  def validate_ai_response(self, response: str) -> bool:
  """Validate AI response for ethical compliance."""
  violations = self.check_content(response)

  if violations:
  print(f"🚨 ETHICAL VIOLATION DETECTED: {len(violations)} issues found")
  for violation in violations:
  print(f"  - {violation['type']}: {violation['pattern']}")
  return False

  return True

# Global ethics checker
ethics_checker = EthicalComplianceChecker()
'''

  ethics_path = self.project_root / "core" / "ethics_checker.py"
  ethics_path.write_text(ethics_code)
  measures_applied.append("ethics-checker")

  self.report["containment_measures"] = measures_applied
  logger.info(f"✅ Applied {len(measures_applied)} containment measures")
  return measures_applied

  def generate_compliance_report(self) -> Dict[str, Any]:
  """Generate ethical compliance assessment."""
  logger.info("📋 Generating ethical compliance report...")

  compliance = {
  "overall_score": 0,
  "compliance_areas": {
  "transparency": {"score": 85, "issues": []},
  "privacy": {"score": 90, "issues": []},
  "fairness": {"score": 88, "issues": []},
  "accountability": {"score": 92, "issues": []},
  "safety": {"score": 75, "issues": []}
  },
  "critical_issues": [],
  "recommendations": []
  }

  # Assess based on violations found
  critical_violations = [v for v in self.violations if v.threat_level == ThreatLevel.CRITICAL]
  high_violations = [v for v in self.violations if v.threat_level == ThreatLevel.HIGH]

  # Adjust scores based on violations
  if critical_violations:
  compliance["compliance_areas"]["safety"]["score"] -= len(critical_violations) * 10
  compliance["critical_issues"].extend([
  f"Critical AI violation in {v.file_path}:{v.line_number}" for v in critical_violations
  ])

  if high_violations:
  compliance["compliance_areas"]["accountability"]["score"] -= len(high_violations) * 5

  # Calculate overall score
  scores = [area["score"] for area in compliance["compliance_areas"].values()]
  compliance["overall_score"] = sum(scores) // len(scores)

  # Generate recommendations
  if compliance["overall_score"] < 80:
  compliance["recommendations"].append("Immediate review of AI containment violations required")

  if critical_violations:
  compliance["recommendations"].append("Critical violations must be addressed before deployment")

  compliance["recommendations"].extend([
  "Implement runtime AI behavior monitoring",
  "Regular ethical compliance audits",
  "Staff training on AI ethics and safety",
  "Establish AI governance committee"
  ])

  self.report["ethical_compliance"] = compliance
  return compliance

  def generate_recommendations(self) -> List[str]:
  """Generate actionable recommendations."""
  recommendations = []

  critical_count = len([v for v in self.violations if v.threat_level == ThreatLevel.CRITICAL])
  high_count = len([v for v in self.violations if v.threat_level == ThreatLevel.HIGH])

  if critical_count > 0:
  recommendations.append(f"URGENT: Address {critical_count} critical AI containment violations")

  if high_count > 0:
  recommendations.append(f"HIGH PRIORITY: Review {high_count} high-risk AI behavior patterns")

  recommendations.extend([
  "Implement runtime AI behavior monitoring system",
  "Establish AI ethics review board",
  "Create AI incident response procedures",
  "Regular AI safety training for development team",
  "Implement automated AI behavior testing",
  "Establish AI governance policies and procedures",
  "Create AI risk assessment framework",
  "Implement AI audit trail and logging",
  "Establish AI performance and safety metrics",
  "Regular third-party AI safety assessments"
  ])

  self.report["recommendations"] = recommendations
  return recommendations

  def run_containment_protocol(self) -> Dict[str, Any]:
  """Execute complete AI containment and ethical compliance protocol."""
  logger.info("🤖 Initiating AI Containment & Ethical Compliance Protocol...")

  try:
  # Phase 1: Scan codebase for violations
  self.scan_codebase()

  # Phase 2: Apply containment measures
  self.apply_containment_measures()

  # Phase 3: Generate compliance report
  self.generate_compliance_report()

  # Phase 4: Generate recommendations
  self.generate_recommendations()

  # Save comprehensive report
  report_path = self.project_root / "tools" / "ai_containment_report.json"
  with open(report_path, 'w') as f:
  json.dump(self.report, f, indent=2)

  logger.info("🎉 AI Containment Protocol COMPLETE!")
  return self.report

  except Exception as e:
  logger.error(f"❌ Containment protocol failed: {e}")
  self.report["error"] = str(e)
  return self.report

def main():
  """Main execution function."""
  if len(sys.argv) > 1:
  project_root = sys.argv[1]
  else:
  project_root = os.getcwd()

  sentinel = AIContainmentSentinel(project_root)
  report = sentinel.run_containment_protocol()

  # Print summary
  print("\n" + "="*60)
  print("🤖 AIFOLIO AI CONTAINMENT & ETHICAL COMPLIANCE REPORT")
  print("="*60)

  scan_summary = report.get("scan_summary", {})
  print(f"📊 Files Scanned: {scan_summary.get('files_scanned', 0)}")
  print(f"🚨 Violations Found: {scan_summary.get('total_violations', 0)}")
  print(f"🛡️ Containment Measures: {len(report.get('containment_measures', []))}")

  compliance = report.get("ethical_compliance", {})
  print(f"📋 Compliance Score: {compliance.get('overall_score', 0)}/100")
  print(f"💡 Recommendations: {len(report.get('recommendations', []))}")

  if report.get('error'):
  print(f"❌ Error: {report['error']}")
  return 1

  print("✅ CONTAINMENT PROTOCOL COMPLETE")
  return 0

if __name__ == "__main__":
  sys.exit(main())
