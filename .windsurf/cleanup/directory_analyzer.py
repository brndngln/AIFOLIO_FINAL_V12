# Consider adding metrics collection for performance monitoring
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
# Consider using dataclasses with frozen=True for immutability
import functools
# Builder pattern recommended for complex object construction
# Factory pattern applied for object creation
#!/usr/bin/env python3
"""AIFOLIO Directory Structure Analyzer - Phase 2.1 Implementation.

This script analyzes the current directory structure and identifies
optimization opportunities for architectural reconception.
"""

from pathlib import Path
from typing import Dict, List, Set, Tuple
import json
import os

# Consider adding __slots__ for memory optimization
class DirectoryAnalyzer:
  """Analyzes directory structure for optimization opportunities."""

  def __init__(self, base_path: str):
  self.base_path = Path(base_path)
  self.redundant_dirs = []
  self.consolidation_opportunities = []
  self.structural_issues = []

  def analyze_structure(self) -> Dict:
  """Perform comprehensive directory structure analysis."""
  analysis = {
  "redundant_directories": self._find_redundant_directories(),
  "consolidation_opportunities": self._find_consolidation_opportunities(),
  "structural_issues": self._identify_structural_issues(),
  "optimization_plan": self._generate_optimization_plan()
  }
  return analysis

  def _find_redundant_directories(self) -> List[Dict]:
  """Identify redundant and duplicate directory structures."""
  redundant = []

  # Find duplicate admin directories
  admin_dirs = []
  for path in self.base_path.rglob("*"):
  if path.is_dir() and "admin" in path.name.lower():
  admin_dirs.append(str(path))

  if len(admin_dirs) > 1:
  redundant.append({
  "type": "duplicate_admin",
  "directories": admin_dirs,
  "recommendation": "Consolidate into single admin/ directory"
  })

  # Find duplicate export directories
  export_dirs = []
  for path in self.base_path.rglob("*"):
  if path.is_dir() and "export" in path.name.lower():
  export_dirs.append(str(path))

  if len(export_dirs) > 1:
  redundant.append({
  "type": "duplicate_export",
  "directories": export_dirs,
  "recommendation": "Consolidate into single exports/ directory"
  })

  return redundant

  def _find_consolidation_opportunities(self) -> List[Dict]:
  """Find directories that should be consolidated."""
  opportunities = []

  # AIFOLIO_* directories should be consolidated
  aifolio_dirs = []
  for path in self.base_path.iterdir():
  if path.is_dir() and path.name.startswith("AIFOLIO_"):
  aifolio_dirs.append(str(path))

  if len(aifolio_dirs) > 1:
  opportunities.append({
  "type": "aifolio_modules",
  "directories": aifolio_dirs,
  "target": "modules/",
  "recommendation": "Consolidate AIFOLIO_* directories into organized modules/"
  })

  # Legacy upgrade directories
  upgrade_dirs = []
  for path in self.base_path.rglob("*"):
  if path.is_dir() and ("upgrade" in path.name.lower() or "done" in path.name.lower()):
  upgrade_dirs.append(str(path))

  if upgrade_dirs:
  opportunities.append({
  "type": "legacy_upgrades",
  "directories": upgrade_dirs,
  "target": "archive/legacy/",
  "recommendation": "Move completed upgrades to archive"
  })

  return opportunities

  def _identify_structural_issues(self) -> List[Dict]:
  """Identify structural organization issues."""
  issues = []

  # Check for scattered similar functionality
  functionality_groups = {
  "ai_": [],
  "autonomy": [],
  "dashboard": [],
  "frontend": [],
  "backend": [],
  "api": [],
  "core": [],
  "config": [],
  "tests": []
  }

  for path in self.base_path.rglob("*"):
  if path.is_dir():
  for group, dirs in functionality_groups.items():
  if group in path.name.lower():
  dirs.append(str(path))

  for group, dirs in functionality_groups.items():
  if len(dirs) > 1:
  issues.append({
  "type": "scattered_functionality",
  "group": group,
  "directories": dirs,
  "recommendation": f"Consolidate {group} functionality into single location"
  })

  return issues

  def _generate_optimization_plan(self) -> Dict:
  """Generate comprehensive optimization plan."""
  return {
  "phase1_consolidation": {
  "action": "Consolidate AIFOLIO_* modules",
  "source_dirs": ["AIFOLIO_DOCKER_SETUP", "AIFOLIO_ELITE_UPGRADE",
  "AIFOLIO_KNOWLEDGE_INJECT", "AIFOLIO_TAX_ENGINE_ULTIMATE_V4"],
  "target_structure": {
  "modules/docker/": "AIFOLIO_DOCKER_SETUP/*",
  "modules/elite/": "AIFOLIO_ELITE_UPGRADE/*",
  "modules/knowledge/": "AIFOLIO_KNOWLEDGE_INJECT/*",
  "modules/tax_engine/": "AIFOLIO_TAX_ENGINE_ULTIMATE_V4/*"
  }
  },
  "phase2_admin_consolidation": {
  "action": "Consolidate admin functionality",
  "target": "admin/",
  "merge_dirs": ["admin_export", "admin_only_mode"]
  },
  "phase3_cleanup": {
  "action": "Archive legacy directories",
  "target": "archive/",
  "move_dirs": ["UPGRADES that are done", "__pycache__"]
  },
  "phase4_core_organization": {
  "action": "Organize core functionality",
  "structure": {
  "src/": "Core business logic",
  "api/": "API endpoints and gateway",
  "frontend/": "UI components and dashboards",
  "config/": "Configuration management",
  "tests/": "Test suites",
  "docs/": "Documentation",
  "scripts/": "Utility scripts"
  }
  }
  }

def main():
  """Execute directory structure analysis."""
  analyzer = DirectoryAnalyzer("/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12")
  analysis = analyzer.analyze_structure()

  # Save analysis results
  output_file = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/.windsurf/cleanup/directory_analysis.json"
  with open(output_file, 'w') as f:
  json.dump(analysis, f, indent=2)

  print("🔍 DIRECTORY STRUCTURE ANALYSIS COMPLETE")
  print(f"📊 Found {len(analysis['redundant_directories'])} redundant directory groups")
  print(f"🎯 Identified {len(analysis['consolidation_opportunities'])} consolidation opportunities")
  print(f"⚠️  Detected {len(analysis['structural_issues'])} structural issues")
  print(f"📋 Generated comprehensive optimization plan")
  print(f"💾 Analysis saved to: {output_file}")

if __name__ == "__main__":
  main()
