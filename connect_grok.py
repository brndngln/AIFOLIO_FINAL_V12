import os
from xai_sdk import Client
from xai_sdk.chat import user, system

# Directories to ignore (no changes needed—it's working)
ignored_dirs = [
    "quarantine_non_python",
    "corrupted_black_failures",
    "windsurf_backup_replaced",
    "repair_backup",
    "backup_broken",
    ".venv",
    "__pycache__",
    ".git",
    ".backups",
    "windsurf_regen_failed",
    "AIFOLIO_KNOWLEDGE_INJECT",  # Excludes duplicates
    # Add others if needed
]

# Load codebase files, skipping ignored dirs
codebase_files = []
for root, dirs, files in os.walk("."):
    # Prune ignored subdirs
    dirs[:] = [d for d in dirs if d not in ignored_dirs]

    for file in files:
        if file.endswith((".py", ".js", ".html", ".css")):  # Customize if needed
            full_path = os.path.join(root, file)
            codebase_files.append(full_path)

# Sort files by size and print top 20
file_sizes = [(f, os.path.getsize(f) / (1024 * 1024)) for f in codebase_files]
file_sizes.sort(key=lambda x: x[1], reverse=True)
print("Top 20 largest files (MB):")
for f, size in file_sizes[:20]:
    print(f"{size:.2f} MB - {f}")

# Total size and count
total_size_mb = sum(s for _, s in file_sizes)
print(f"\nTotal codebase size: {total_size_mb:.2f} MB")
print(f"Number of files: {len(codebase_files)}")

# Rough token estimate (avg 4 chars/token)
approx_tokens = int(total_size_mb * 1024 * 1024 / 4)
print(f"Approximate tokens: {approx_tokens}")

# If too big, stop
if total_size_mb > 20 or approx_tokens > 250000:
    print("WARNING: Still too large! Add more to ignored_dirs.")
    exit(1)

# Load as string
codebase = "\n\n".join(f"File: {f}\n" + open(f, "r").read() for f in codebase_files)

# API call with error handling
try:
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(model="grok-4-0709")  # Correct model name
    chat.append(system("Analyze this codebase: " + codebase))
    chat.append(
        user(
            "Provide a detailed summary of the codebase, including main components, technologies used, structure, and any notable features like dashboards, backend elements, or tests."
        )
    )

    response = chat.sample()
    print("\nGrok-4 Summary:\n")
    print(response.content)
except Exception as e:
    print(f"API Error: {str(e)}")
    print(
        "Check your API key, subscription (Grok-4 requires SuperGrok or Premium+), or visit https://x.ai/api for details."
    )
