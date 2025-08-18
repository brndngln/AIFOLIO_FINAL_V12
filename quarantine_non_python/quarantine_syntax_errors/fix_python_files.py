import ast
import os

base_dir = os.getcwd()
quarantine_dir = os.path.join(base_dir, "quarantine_non_python")
fix_log_path = os.path.join(base_dir, "fix_log.txt")
os.makedirs(quarantine_dir, exist_ok=True)
log_entries = []
for root, _, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".py"):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                if "expected an indented block" in str(e) or "unexpected EOF" in str(e):
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if line.strip().endswith(":") and (
                            i == len(lines) - 1 or lines[i + 1].strip() == ""
                        ):
                            lines.insert(i + 1, "    pass")
                    try:
                        fixed_content = "\n".join(lines)
                        ast.parse(fixed_content)
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(fixed_content)
                        log_entries.append(f"AUTO-FIXED: {file_path}")
                    except SyntaxError:
                        quarantine_path = os.path.join(
                            quarantine_dir, os.path.relpath(file_path, base_dir)
                        )
                        os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
                        os.rename(file_path, quarantine_path)
                        log_entries.append(f"QUARANTINED (still broken): {file_path}")
                else:
                    quarantine_path = os.path.join(
                        quarantine_dir, os.path.relpath(file_path, base_dir)
                    )
                    os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
                    os.rename(file_path, quarantine_path)
                    log_entries.append(f"QUARANTINED (invalid syntax): {file_path}")
            except Exception as e:
                log_entries.append(f"ERROR: {file_path} — {str(e)}")
with open(fix_log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_entries))
print(f"✅ Fix complete. Log saved to {fix_log_path}")
