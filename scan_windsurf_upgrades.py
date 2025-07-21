import os

# SAFE AI: This script is non-sentient, static, deterministic, owner-controlled, and audit-compliant.

# Keywords to search for in file paths/names (case-insensitive)
keywords = ["windsurf", "upgrade", "regen"]  # Add more like 'ai_regen' if needed

# Collect matching files with metadata
matching_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        full_path = os.path.join(root, file)
        if any(kw.lower() in full_path.lower() for kw in keywords):
            stat = os.stat(full_path)
            matching_files.append(
                {
                    "path": full_path,
                    "mtime": stat.st_mtime,  # Last modified time
                    "size_mb": stat.st_size / (1024 * 1024),  # Size in MB
                }
            )

# Sort by mtime descending (newest first)
sorted_files = sorted(matching_files, key=lambda x: x["mtime"], reverse=True)

# Print as table
print("| Last Modified | Size (MB) | Path |")
print("|---------------|-----------|------|")
for f in sorted_files:
    mod_time = datetime.fromtimestamp(f["mtime"]).strftime("%Y-%m-%d %H:%M:%S")
    print(f"| {mod_time} | {f['size_mb']:.2f} | {f['path']} |")

if not sorted_files:
    print(
        "No matching files found. Try adjusting keywords or check if Windsurf logs are in a different format."
    )
