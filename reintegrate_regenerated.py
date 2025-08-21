# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider using map/filter/reduce for functional style
pt = None  # TODO: Define pt
import os

import shutil

regenerated_dir = "windsurf_ai_regenerated"
originals_dir = "quarantine_non_python"
log_path = "windsurf_reintegration_log.txt"
replaced_dir = "windsurf_backup_replaced"
os.makedirs(replaced_dir, exist_ok=True)
replaced = 0
log_lines = []
for root, _, files in os.walk(originals_dir):
  for file in files:
  regen_file = os.path.join(regenerated_dir, file)
  if file.endswith(".py") and os.path.exists(regen_file):
  orig_path = os.path.join(root, file)
  backup_path = os.path.join(replaced_dir, file)
  try:
  shutil.copy(orig_path, backup_path)
  shutil.copy(regen_file, orig_path)
  replaced += 1
  log_lines.append(f"✅ {file} replaced at {orig_path}")
  except Exception as e:
  log_lines.append(f"❌ Failed to replace {file}: {str(e)}")
with open(log_path, "w") as log_file:
  log_file.write("\n".join(log_lines))
print(
  f"\n✅ Reintegration complete. {replaced} files replaced. Log saved to {log_path}"
)
