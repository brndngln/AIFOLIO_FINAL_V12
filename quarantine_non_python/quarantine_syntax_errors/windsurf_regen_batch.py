import ast
import os
import re
import shutil

regen_dir = "windsurf_regen_queue"
failed_dir = "windsurf_regen_failed"
log_path = "windsurf_repair_log.txt"
os.makedirs(failed_dir, exist_ok=True)
repaired = 0
failed = 0
log_lines = []


def fix_syntax_issues(code):
    lines = code.split("\n")
    fixed_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        fixed_lines.append(line)
        if re.match("^(if|for|while|elif|else|try|except|with).*:\\s*$", stripped):
            if i + 1 >= len(lines) or lines[i + 1].strip() == "":
                fixed_lines.append("    pass")
    return "\n".join(fixed_lines)


for file in os.listdir(regen_dir):
    if file.endswith(".py"):
        full_path = os.path.join(regen_dir, file)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                code = f.read()
            code = fix_syntax_issues(code)
            try:
                ast.parse(code)
            except SyntaxError:
                raise SyntaxError("Still invalid after syntax patching.")
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)
            log_lines.append(f"[✅ FIXED] {file}")
            repaired += 1
        except Exception as e:
            failed_path = os.path.join(failed_dir, file)
            shutil.copy(full_path, failed_path)
            log_lines.append(f"[❌ FAILED] {file} - {str(e)}")
            failed += 1
with open(log_path, "w") as log:
    log.write("\n".join(log_lines))
print(
    f"✅ Windsurf regen complete. {repaired} files fixed, {failed} failed. Log saved to {log_path}"
)
