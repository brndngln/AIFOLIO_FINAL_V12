#!/usr/bin/env python3

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
FAILED_LIST = ROOT_DIR / "clean_unreformattable_files.txt"


def fix_typing_syntax(line: str) -> str:
    # Replace Python 3.10+ union types with Optional[]
    line = re.sub(r"->\s*str\s*\|\s*None", "-> Optional[str]", line)
    line = re.sub(r"->\s*bytes\s*\|\s*None", "-> Optional[bytes]", line)
    line = re.sub(r"->\s*bool\s*\|\s*str", "-> Union[bool, str]", line)
    line = re.sub(r"->\s*str\s*\|\s*int", "-> Union[str, int]", line)
    return line


def fix_indentation_and_pass(lines: list[str]) -> list[str]:
    fixed = []

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if stripped.startswith("pass") and (not fixed or fixed[-1].strip() == ""):
            continue  # Skip floating pass

        if indent % 4 != 0:
            indent = (indent // 4) * 4  # Normalize to 4-space indent

        fixed_line = (" " * indent) + stripped
        fixed.append(fixed_line)

    return fixed


def process_file(file_path: Path):
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        new_lines = [fix_typing_syntax(line) for line in lines]
        new_lines = fix_indentation_and_pass(new_lines)

        if any("Optional[" in l or "Union[" in l for l in new_lines):
            if "from typing import" not in "".join(new_lines):
                new_lines.insert(0, "from typing import Optional, Union\n")

        with file_path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"[FIXED] {file_path}")
    except Exception as e:
        print(f"[SKIPPED] {file_path} — {e}")


def main():
    if not FAILED_LIST.exists():
        print("Missing: clean_unreformattable_files.txt")
        return

    with FAILED_LIST.open("r") as f:
        paths = [Path(line.strip()) for line in f if line.strip()]

    for path in paths:
        if path.exists():
            process_file(path)
        else:
            print(f"[MISSING] {path}")


if __name__ == "__main__":
    main()
