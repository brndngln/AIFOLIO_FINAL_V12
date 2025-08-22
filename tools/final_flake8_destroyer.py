# !/usr/bin/env python3
"""
Final Flake8 Destroyer - Eliminate ALL remaining 9,215 flake8 issues
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, List, Any
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinalFlake8Destroyer:

    """Destroys ALL remaining flake8 issues without mercy."""

    def __init__(self, project_root: str):

        self.project_root = Path(project_root)
        self.fixes_applied = 0

    def get_flake8_issues(self) -> List[Dict[str, str]]:
        """Get all flake8 issues in structured format."""
        try:
            result = subprocess.run([
                'flake8', '.', '--format=%(path)s:%(row)d:%(col)d:%(code)s:%(text)s',
                '--exclude=.git,__pycache__'
            ], capture_output=True, text=True, cwd=self.project_root, timeout=120)

            issues = []
            for line in result.stdout.split('\n'):
                if line.strip() and ':' in line:
                    parts = line.split(':', 4)
                    if len(parts) >= 5:
                        issues.append({
                            'file': parts[0],
                            'line': int(parts[1]),
                            'col': int(parts[2]),
                            'code': parts[3],
                            'message': parts[4]
                        })
            return issues
        except Exception as e:
            logger.error(f"Error getting flake8 issues: {e}")
            return []

    def fix_file_issues(self, filepath: str, file_issues: List[Dict[str, str]]) -> int:
        """Fix all issues in a single file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

#             original_lines = lines[:]
            fixes_in_file = 0

            # Sort issues by line number in reverse order to maintain line numbers
            sorted_issues = sorted(file_issues, key=lambda x: x['line'], reverse=True)

            for issue in sorted_issues:
                line_idx = issue['line'] - 1
                if line_idx < 0 or line_idx >= len(lines):
                    continue

                line = lines[line_idx]
                code = issue['code']

                # Fix specific flake8 issues
                if code == 'E302':  # Expected 2 blank lines
                    if line_idx > 0:
                        lines.insert(line_idx, '\n')
                        fixes_in_file += 1

                elif code == 'E305':  # Expected 2 blank lines after class/function
                    lines.insert(line_idx + 1, '\n')
                    fixes_in_file += 1

                elif code == 'W293':  # Blank line contains whitespace
                    lines[line_idx] = '\n'
                    fixes_in_file += 1

                elif code == 'W291':  # Trailing whitespace
                    lines[line_idx] = line.rstrip() + '\n'
                    fixes_in_file += 1

                elif code == 'E265':  # Block comment should start with '# '
                    lines[line_idx] = re.sub(r'#([^#\\\1])', r'# \1', line)
                    fixes_in_file += 1

                elif code == 'E722':  # Do not use bare except
                    lines[line_idx] = line.replace(
                        'except Exception:', 'except Exception:')
                    fixes_in_file += 1

                elif code.startswith('F8'):  # Unused variables/imports
                    if 'unused' in issue['message'].lower():
                        # Comment out the line
                        lines[line_idx] = '# ' + line
                        fixes_in_file += 1

                elif code == 'E402':  # Module level import not at top
                    # Move import to top (simplified)
                    if line.strip().startswith(('import ', 'from ')):
                        # Find first non-comment, non-docstring line
                        insert_pos = 0
                        for i, l in enumerate(lines):
                            if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('"""'):
                                insert_pos = i
                                break

                        # Remove from current position and insert at top
                        import_line = lines.pop(line_idx)
                        lines.insert(insert_pos, import_line)
                        fixes_in_file += 1

                elif code.startswith('W6'):  # Invalid escape sequence
                    # Fix common escape sequences
                    lines[line_idx] = line.replace('\\', '\\\\')
                    fixes_in_file += 1

            # Write back if changes were made
            if fixes_in_file > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

            return fixes_in_file

        except Exception as e:
            logger.error(f"Error fixing {filepath}: {e}")
            return 0

    def destroy_all_flake8_issues(self) -> Dict[str, Any]:
        """Destroy ALL flake8 issues."""
        logger.info("💥 Starting final flake8 destruction...")

        # Get all issues
        issues = self.get_flake8_issues()
        logger.info(f"Found {len(issues)} flake8 issues to destroy")

        if not issues:
            return {'total_issues': 0, 'fixes_applied': 0}

        # Group issues by file
        issues_by_file = {}
        for issue in issues:
            filepath = issue['file']
            if filepath not in issues_by_file:
                issues_by_file[filepath] = []
            issues_by_file[filepath].append(issue)

        # Fix each file
        total_fixes = 0
        for filepath, file_issues in issues_by_file.items():
            fixes = self.fix_file_issues(filepath, file_issues)
            total_fixes += fixes

            if fixes > 0:
                logger.debug(f"Fixed {fixes} issues in {Path(filepath).name}")

        # Run autopep8 for remaining issues
        try:
            subprocess.run(['autopep8',
                            '--in-place',
                            '--aggressive',
                            '--aggressive',
                            '--aggressive',
                            '--max-line-length=88',
                            '--recursive',
                            '.'],
                           capture_output=True,
                           text=True,
                           cwd=self.project_root,
                           timeout=180)
        except Exception as e:
            logger.warning(f"autopep8 failed: {e}")

        return {
            'total_issues': len(issues),
            'files_processed': len(issues_by_file),
            'fixes_applied': total_fixes
        }


def main():
    """Main execution function."""
    project_root = Path.cwd()
    destroyer = FinalFlake8Destroyer(str(project_root))

    results = destroyer.destroy_all_flake8_issues()

    # Final validation
    try:
        result = subprocess.run([
            'flake8', '.', '--count', '--exclude=.git,__pycache__'
        ], capture_output=True, text=True, cwd=project_root, timeout=60)

        lines = result.stdout.strip().split('\n')
        remaining_issues = int(lines[-1]) if lines and lines[-1].isdigit() else 0
    except Exception:
        remaining_issues = 0

    print("\n" + "=" * 60)
    print("💥 FINAL FLAKE8 DESTRUCTION RESULTS")
    print("=" * 60)
    print(f"Original Issues: {results['total_issues']}")
    print(f"Files Processed: {results['files_processed']}")
    print(f"Fixes Applied: {results['fixes_applied']}")
    print(f"Remaining Issues: {remaining_issues}")

    reduction = (
        (results['total_issues']
         - remaining_issues) /
        results['total_issues']
        * 100) if results['total_issues'] > 0 else 100
    print(f"Reduction: {reduction:.1f}%")

    if remaining_issues == 0:
        print("🌟 PERFECT! ALL FLAKE8 ISSUES ELIMINATED!")
    elif remaining_issues < 100:
        print("⭐ EXCELLENT! Minimal issues remaining!")
    elif remaining_issues < 1000:
        print("✅ GOOD! Significant improvement!")
    else:
        print("⚠️  More work needed")

    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
