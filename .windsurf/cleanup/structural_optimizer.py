# Consider adding metrics collection for performance monitoring
# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
# Consider using dataclasses with frozen=True for immutability
import functools
# Builder pattern recommended for complex object construction
# Factory pattern applied for object creation
#!/usr/bin/env python3
"""AIFOLIO Structural Optimizer - Phase 2 Implementation.

This script executes the comprehensive directory restructuring plan
based on the analysis results to achieve optimal architectural organization.
"""

from pathlib import Path
from typing import Dict, List
import json
import os

import shutil

# Consider adding __slots__ for memory optimization
class StructuralOptimizer:
  """Executes structural optimization based on analysis results."""

  def __init__(self, base_path: str):
  self.base_path = Path(base_path)
  self.moved_items = []
  self.created_dirs = []
  self.errors = []

  def execute_optimization(self) -> Dict:
  """Execute the complete structural optimization plan."""
  print("🚀 PHASE 2: STRUCTURAL OPTIMIZATION INITIATED")

  # Phase 1: Remove quarantine and backup directories
  self._cleanup_quarantine_directories()

  # Phase 2: Consolidate AIFOLIO modules
  self._consolidate_aifolio_modules()

  # Phase 3: Organize core functionality
  self._organize_core_structure()

  # Phase 4: Clean up legacy directories
  self._cleanup_legacy_directories()

  # Phase 5: Create optimal directory structure
  self._create_optimal_structure()

  return {
  "moved_items": len(self.moved_items),
  "created_directories": len(self.created_dirs),
  "errors": len(self.errors),
  "status": "completed"
  }

  def _cleanup_quarantine_directories(self):
  """Remove quarantine and backup directories that cause structural bloat."""
  print("🧹 Cleaning up quarantine and backup directories...")

  quarantine_dirs = [
  "quarantine_non_python",
  ".windsurf/synth/backups",
  ".windsurf/synth/specs",
  ".mypy_cache"
  ]

  for dir_name in quarantine_dirs:
  dir_path = self.base_path / dir_name
  if dir_path.exists():
  try:
  shutil.rmtree(dir_path)
  print(f"  ✅ Removed: {dir_name}")
  except Exception as e:
  self.errors.append(f"Failed to remove {dir_name}: {e}")
  print(f"  ❌ Error removing {dir_name}: {e}")

  def _consolidate_aifolio_modules(self):
  """Consolidate AIFOLIO_* directories into organized modules structure."""
  print("📦 Consolidating AIFOLIO modules...")

  # Create modules directory
  modules_dir = self.base_path / "modules"
  modules_dir.mkdir(exist_ok=True)
  self.created_dirs.append("modules/")

  # Module mappings
  module_mappings = {
  "AIFOLIO_DOCKER_SETUP": "modules/docker",
  "AIFOLIO_ELITE_UPGRADE": "modules/elite",
  "AIFOLIO_KNOWLEDGE_INJECT": "modules/knowledge",
  "AIFOLIO_TAX_ENGINE_ULTIMATE_V4": "modules/tax_engine"
  }

  for source_name, target_path in module_mappings.items():
  source_dir = self.base_path / source_name
  target_dir = self.base_path / target_path

  if source_dir.exists():
  try:
  # Create target directory
  target_dir.parent.mkdir(parents=True, exist_ok=True)

  # Move the directory
  shutil.move(str(source_dir), str(target_dir))
  self.moved_items.append(f"{source_name} → {target_path}")
  print(f"  ✅ Moved: {source_name} → {target_path}")
  except Exception as e:
  self.errors.append(f"Failed to move {source_name}: {e}")
  print(f"  ❌ Error moving {source_name}: {e}")

  def _organize_core_structure(self):
  """Organize core functionality into proper structure."""
  print("🏗️  Organizing core structure...")

  # Create core directories (check for existing files first)
  core_dirs = [
  "src/core",
  "src/api",
  "src/services",
  "src/utils",
  "config/environments",
  "scripts/deploy",
  "scripts/maintenance",
  "tests/unit",
  "tests/integration",
  "docs/api",
  "docs/deploy"
  ]

  for dir_path in core_dirs:
  full_path = self.base_path / dir_path
  parent_path = full_path.parent

  # Check if parent path exists as file and remove it
  if parent_path.exists() and parent_path.is_file():
  parent_path.unlink()
  print(f"  🗑️  Removed conflicting file: {parent_path.name}")

  # Check if path exists as file and remove it
  if full_path.exists() and full_path.is_file():
  full_path.unlink()
  print(f"  🗑️  Removed conflicting file: {dir_path}")

  try:
  full_path.mkdir(parents=True, exist_ok=True)
  self.created_dirs.append(dir_path)
  print(f"  ✅ Created: {dir_path}")
  except Exception as e:
  self.errors.append(f"Failed to create {dir_path}: {e}")
  print(f"  ❌ Error creating {dir_path}: {e}")

  # Move core files to appropriate locations
  core_moves = {
  "aifolio.py": "src/core/aifolio.py",
  "custom_ast_module.py": "src/utils/custom_ast_module.py",
  "ImageFile.py": "src/utils/image_processing.py"
  }

  for source, target in core_moves.items():
  source_path = self.base_path / source
  target_path = self.base_path / target

  if source_path.exists():
  try:
  target_path.parent.mkdir(parents=True, exist_ok=True)
  shutil.move(str(source_path), str(target_path))
  self.moved_items.append(f"{source} → {target}")
  print(f"  ✅ Moved: {source} → {target}")
  except Exception as e:
  self.errors.append(f"Failed to move {source}: {e}")
  print(f"  ❌ Error moving {source}: {e}")

  def _cleanup_legacy_directories(self):
  """Clean up legacy and completed upgrade directories."""
  print("🗂️  Cleaning up legacy directories...")

  # Create archive directory
  archive_dir = self.base_path / "archive"
  archive_dir.mkdir(exist_ok=True)
  self.created_dirs.append("archive/")

  # Directories to archive
  legacy_dirs = [
  "UPGRADES that are done",
  "done",
  "__pycache__"
  ]

  for dir_name in legacy_dirs:
  source_dir = self.base_path / dir_name
  if source_dir.exists():
  target_dir = archive_dir / dir_name
  try:
  shutil.move(str(source_dir), str(target_dir))
  self.moved_items.append(f"{dir_name} → archive/{dir_name}")
  print(f"  ✅ Archived: {dir_name}")
  except Exception as e:
  self.errors.append(f"Failed to archive {dir_name}: {e}")
  print(f"  ❌ Error archiving {dir_name}: {e}")

  def _create_optimal_structure(self):
  """Create the final optimal directory structure."""
  print("🎯 Creating optimal directory structure...")

  # Consolidate admin functionality
  admin_dirs = ["admin_export", "admin_only_mode"]
  admin_target = self.base_path / "admin"
  admin_target.mkdir(exist_ok=True)

  for admin_dir in admin_dirs:
  source_dir = self.base_path / admin_dir
  if source_dir.exists():
  target_dir = admin_target / admin_dir.replace("admin_", "")
  try:
  shutil.move(str(source_dir), str(target_dir))
  self.moved_items.append(f"{admin_dir} → admin/{admin_dir.replace('admin_', '')}")
  print(f"  ✅ Consolidated: {admin_dir} → admin/")
  except Exception as e:
  self.errors.append(f"Failed to consolidate {admin_dir}: {e}")
  print(f"  ❌ Error consolidating {admin_dir}: {e}")

  # Consolidate export functionality
  export_dirs = ["data_export"]
  exports_target = self.base_path / "exports"
  exports_target.mkdir(exist_ok=True)

  for export_dir in export_dirs:
  source_dir = self.base_path / export_dir
  if source_dir.exists():
  target_dir = exports_target / export_dir.replace("_export", "")
  try:
  shutil.move(str(source_dir), str(target_dir))
  self.moved_items.append(f"{export_dir} → exports/{export_dir.replace('_export', '')}")
  print(f"  ✅ Consolidated: {export_dir} → exports/")
  except Exception as e:
  self.errors.append(f"Failed to consolidate {export_dir}: {e}")
  print(f"  ❌ Error consolidating {export_dir}: {e}")

  # Consolidate AI functionality
  ai_dirs = ["ai_engines", "ai_logic", "ai_tools", "ai_behavior_profiles", "aifolio_ai_bots_backend", "ai_core"]
  ai_target = self.base_path / "src/ai"
  ai_target.mkdir(parents=True, exist_ok=True)

  for ai_dir in ai_dirs:
  source_dir = self.base_path / ai_dir
  if source_dir.exists():
  target_dir = ai_target / ai_dir.replace("aifolio_", "").replace("ai_", "")
  try:
  shutil.move(str(source_dir), str(target_dir))
  self.moved_items.append(f"{ai_dir} → src/ai/{ai_dir.replace('aifolio_', '').replace('ai_', '')}")
  print(f"  ✅ Consolidated: {ai_dir} → src/ai/")
  except Exception as e:
  self.errors.append(f"Failed to consolidate {ai_dir}: {e}")
  print(f"  ❌ Error consolidating {ai_dir}: {e}")

def main():
  """Execute structural optimization."""
  optimizer = StructuralOptimizer("/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12")
  results = optimizer.execute_optimization()

  print("\n" + "="*60)
  print("🎯 PHASE 2: STRUCTURAL OPTIMIZATION COMPLETE")
  print("="*60)
  print(f"📦 Items moved: {results['moved_items']}")
  print(f"📁 Directories created: {results['created_directories']}")
  print(f"❌ Errors encountered: {results['errors']}")
  print(f"✅ Status: {results['status'].upper()}")

  if optimizer.errors:
  print("\n⚠️  ERRORS ENCOUNTERED:")
  for error in optimizer.errors:
  print(f"  • {error}")

  print("\n🚀 AIFOLIO codebase structure optimized for maximum clarity and maintainability!")

if __name__ == "__main__":
  main()
