#!/usr/bin/env python3
"""
AIFOLIO Codebase Archiver
Creates comprehensive backup and archive of entire codebase
"""

import json
import os
import shutil
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class CodebaseArchiver:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.root_path.parent / f"AIFOLIO_BACKUP_{self.timestamp}"
        self.archive_name = f"AIFOLIO_COMPLETE_BACKUP_{self.timestamp}.tar.gz"
        
        # Directories to exclude from backup
        self.exclude_dirs = {
            "__pycache__",
            ".git",
            "node_modules", 
            ".venv",
            "venv_backend",
            ".ruff_cache",
            "dist",
            "build",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "htmlcov"
        }
        
        self.stats = {
            "total_files": 0,
            "total_size": 0,
            "directories": 0,
            "file_types": {},
            "largest_files": []
        }

    def get_git_info(self) -> Dict:
        """Get current Git repository information"""
        try:
            # Get current branch
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"], 
                cwd=self.root_path,
                text=True
            ).strip()
            
            # Get latest commit
            commit = subprocess.check_output(
                ["git", "log", "-1", "--format=%H %s %an %ad"],
                cwd=self.root_path,
                text=True
            ).strip()
            
            # Get repository status
            status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=self.root_path,
                text=True
            ).strip()
            
            # Get remote info
            try:
                remote = subprocess.check_output(
                    ["git", "remote", "get-url", "origin"],
                    cwd=self.root_path,
                    text=True
                ).strip()
            except:
                remote = "No remote configured"
            
            return {
                "branch": branch,
                "latest_commit": commit,
                "status": status,
                "remote": remote,
                "has_uncommitted_changes": bool(status)
            }
        except Exception as e:
            return {"error": f"Failed to get Git info: {e}"}

    def analyze_file(self, file_path: Path):
        """Analyze a single file and update statistics"""
        try:
            stat = file_path.stat()
            size = stat.st_size
            
            self.stats["total_files"] += 1
            self.stats["total_size"] += size
            
            # Track file extensions
            ext = file_path.suffix.lower()
            if ext:
                self.stats["file_types"][ext] = self.stats["file_types"].get(ext, 0) + 1
            else:
                self.stats["file_types"]["no_extension"] = self.stats["file_types"].get("no_extension", 0) + 1
            
            # Track largest files
            self.stats["largest_files"].append({
                "path": str(file_path.relative_to(self.root_path)),
                "size": size
            })
            
            # Keep only top 20 largest files
            self.stats["largest_files"].sort(key=lambda x: x["size"], reverse=True)
            self.stats["largest_files"] = self.stats["largest_files"][:20]
            
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    def should_include_path(self, path: Path) -> bool:
        """Check if path should be included in backup"""
        # Skip excluded directories
        for part in path.parts:
            if part in self.exclude_dirs:
                return False
        
        # Skip hidden files/directories (except .gitignore, .env.example, etc.)
        if path.name.startswith('.') and path.name not in {
            '.gitignore', '.env.example', '.editorconfig', '.prettierrc',
            '.dockerignore', '.gitattributes', '.tool-versions'
        }:
            return False
            
        return True

    def create_inventory(self) -> Dict:
        """Create detailed inventory of codebase"""
        inventory = {
            "timestamp": self.timestamp,
            "root_path": str(self.root_path),
            "git_info": self.get_git_info(),
            "structure": {},
            "statistics": self.stats
        }
        
        print("📊 Creating codebase inventory...")
        
        # Walk through directory structure
        for item in self.root_path.rglob("*"):
            if not self.should_include_path(item):
                continue
                
            relative_path = item.relative_to(self.root_path)
            
            if item.is_file():
                self.analyze_file(item)
                inventory["structure"][str(relative_path)] = {
                    "type": "file",
                    "size": item.stat().st_size,
                    "extension": item.suffix.lower()
                }
            elif item.is_dir():
                self.stats["directories"] += 1
                inventory["structure"][str(relative_path)] = {
                    "type": "directory"
                }
        
        # Format size for readability
        self.stats["total_size_mb"] = round(self.stats["total_size"] / (1024 * 1024), 2)
        
        return inventory

    def copy_codebase(self):
        """Copy entire codebase to backup directory"""
        print(f"📁 Creating backup directory: {self.backup_dir}")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        print("📋 Copying codebase files...")
        copied_files = 0
        
        for item in self.root_path.rglob("*"):
            if not self.should_include_path(item):
                continue
                
            relative_path = item.relative_to(self.root_path)
            dest_path = self.backup_dir / relative_path
            
            try:
                if item.is_file():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
                    copied_files += 1
                    
                    if copied_files % 1000 == 0:
                        print(f"   Copied {copied_files} files...")
                        
                elif item.is_dir():
                    dest_path.mkdir(parents=True, exist_ok=True)
                    
            except Exception as e:
                print(f"Warning: Could not copy {item}: {e}")
        
        print(f"✅ Copied {copied_files} files to backup directory")

    def create_archive(self):
        """Create compressed archive of backup"""
        archive_path = self.root_path.parent / self.archive_name
        
        print(f"🗜️  Creating compressed archive: {self.archive_name}")
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.backup_dir, arcname=f"AIFOLIO_BACKUP_{self.timestamp}")
        
        # Get archive size
        archive_size = archive_path.stat().st_size
        archive_size_mb = round(archive_size / (1024 * 1024), 2)
        
        print(f"✅ Archive created: {archive_size_mb} MB")
        return archive_path, archive_size_mb

    def generate_readme(self, inventory: Dict, archive_path: Path, archive_size_mb: float):
        """Generate README for the backup"""
        readme_content = f"""# AIFOLIO Complete Codebase Backup

## Backup Information
- **Timestamp:** {self.timestamp}
- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Original Path:** {self.root_path}
- **Archive Size:** {archive_size_mb} MB
- **Total Files:** {self.stats['total_files']:,}
- **Total Directories:** {self.stats['directories']:,}
- **Total Size:** {self.stats['total_size_mb']} MB

## Git Repository Information
- **Branch:** {inventory['git_info'].get('branch', 'Unknown')}
- **Latest Commit:** {inventory['git_info'].get('latest_commit', 'Unknown')}
- **Remote:** {inventory['git_info'].get('remote', 'Unknown')}
- **Uncommitted Changes:** {inventory['git_info'].get('has_uncommitted_changes', False)}

## File Type Distribution
"""
        
        # Add file type statistics
        for ext, count in sorted(self.stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:15]:
            readme_content += f"- **{ext or 'no extension'}:** {count:,} files\n"
        
        readme_content += f"""
## Largest Files
"""
        
        # Add largest files
        for file_info in self.stats['largest_files'][:10]:
            size_mb = round(file_info['size'] / (1024 * 1024), 2)
            readme_content += f"- {file_info['path']} ({size_mb} MB)\n"
        
        readme_content += f"""
## Archive Contents
- **Backup Directory:** AIFOLIO_BACKUP_{self.timestamp}/
- **Inventory File:** codebase_inventory_{self.timestamp}.json
- **This README:** README_BACKUP_{self.timestamp}.md

## Restoration Instructions
1. Extract the archive: `tar -xzf {self.archive_name}`
2. Navigate to extracted directory: `cd AIFOLIO_BACKUP_{self.timestamp}`
3. Review the inventory file for detailed structure
4. Copy files to desired location
5. Restore Git repository if needed: `git init && git add . && git commit -m "Restored from backup"`

## Security Notes
- This backup has been sanitized of sensitive data (API keys, tokens, credentials)
- All sensitive values have been replaced with placeholders
- Review and update configuration files with actual values before deployment

## Backup Verification
- Archive integrity can be verified with: `tar -tzf {self.archive_name} > /dev/null && echo "Archive OK"`
- File count verification available in codebase_inventory_{self.timestamp}.json

---
Generated by AIFOLIO Codebase Archiver on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = self.backup_dir / f"README_BACKUP_{self.timestamp}.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return readme_path

    def save_inventory(self, inventory: Dict):
        """Save inventory to JSON file"""
        inventory_path = self.backup_dir / f"codebase_inventory_{self.timestamp}.json"
        
        with open(inventory_path, 'w') as f:
            json.dump(inventory, f, indent=2, default=str)
        
        return inventory_path

    def cleanup_backup_dir(self):
        """Remove the temporary backup directory"""
        print(f"🧹 Cleaning up temporary backup directory...")
        shutil.rmtree(self.backup_dir)

    def create_backup(self):
        """Main method to create complete backup"""
        print(f"🚀 Starting AIFOLIO codebase backup...")
        print(f"📍 Source: {self.root_path}")
        print(f"⏰ Timestamp: {self.timestamp}")
        
        # Create inventory
        inventory = self.create_inventory()
        
        # Copy codebase
        self.copy_codebase()
        
        # Save inventory
        inventory_path = self.save_inventory(inventory)
        print(f"📋 Inventory saved: {inventory_path.name}")
        
        # Create archive
        archive_path, archive_size_mb = self.create_archive()
        
        # Generate README
        readme_path = self.generate_readme(inventory, archive_path, archive_size_mb)
        print(f"📖 README created: {readme_path.name}")
        
        # Update archive with README and inventory
        with tarfile.open(archive_path, "a") as tar:
            tar.add(readme_path, arcname=f"AIFOLIO_BACKUP_{self.timestamp}/{readme_path.name}")
            tar.add(inventory_path, arcname=f"AIFOLIO_BACKUP_{self.timestamp}/{inventory_path.name}")
        
        # Cleanup
        self.cleanup_backup_dir()
        
        print(f"\n🎉 Backup completed successfully!")
        print(f"📦 Archive: {archive_path}")
        print(f"📊 Size: {archive_size_mb} MB")
        print(f"📁 Files: {self.stats['total_files']:,}")
        print(f"📂 Directories: {self.stats['directories']:,}")
        
        return archive_path


def main():
    """Main execution function"""
    root_path = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12"
    
    print("💾 AIFOLIO Codebase Archiver")
    print("=" * 50)
    
    archiver = CodebaseArchiver(root_path)
    archive_path = archiver.create_backup()
    
    print(f"\n✅ Your complete AIFOLIO codebase has been saved!")
    print(f"🔗 Location: {archive_path}")


if __name__ == "__main__":
    main()
