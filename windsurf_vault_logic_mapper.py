import os
import shutil

regen_dir = "windsurf_ai_regenerated"
logic_dir = "vault_logic_templates"
log_path = "windsurf_logic_map_log.txt"
injected = 0
log = []

vault_logic_snippet = """\n
# === VAULT LOGIC START ===
def run_vault_logic():
    print("Vault logic executing...")
# === VAULT LOGIC END ===\n
"""

for root, _, files in os.walk(regen_dir):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if "# WIND_PLACEHOLDER" in content:
                        updated = content.replace(
                            "# WIND_PLACEHOLDER",
                            "# WIND_PLACEHOLDER" + vault_logic_snippet,
                        )
                        f.seek(0)
                        f.write(updated)
                        f.truncate()
                        injected += 1
                        log.append(f"✅ Injected: {full_path}")
            except Exception as e:
                log.append(f"❌ Failed: {full_path} - {e}")

with open(log_path, "w") as f:
    f.write("\n".join(log))

print(f"✅ Logic remap complete. {injected} files updated with vault logic.")
print(f"📄 Log saved to {log_path}")
