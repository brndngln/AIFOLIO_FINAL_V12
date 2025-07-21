import shutil
import subprocess
from pathlib import Path

BROKEN_FILE_LIST = "cleaned_broken_files.txt"
UNREPAIRABLE_LOG = "unrepairable_files.txt"
BACKUP_DIR = "repair_backup"

Path(BACKUP_DIR).mkdir(exist_ok=True)


def is_repairable(path: Path) -> bool:
    try:
        with open(path, "r") as f:
            content = f.read()
        compile(content, str(path), "exec")
        return True
    except Exception:
        return False


def try_repair(file_path: Path) -> bool:
    try:
        # Step 1: Backup
        backup_path = Path(BACKUP_DIR) / file_path.name
        shutil.copy(file_path, backup_path)

        # Step 2: Try autoflake, isort, black
        subprocess.run(
            ["autoflake", "--in-place", "--remove-all-unused-imports", str(file_path)],
            check=False,
        )
        subprocess.run(["isort", str(file_path)], check=False)
        subprocess.run(["black", str(file_path)], check=False)

        # Step 3: Check if now repairable
        return is_repairable(file_path)

    except Exception:
        return False


def main():
    with open(BROKEN_FILE_LIST, "r") as f:
        files = [line.strip() for line in f.readlines()]

    unrepairable = []
    total = len(files)
    print(f"🔧 Attempting to repair {total} broken files...\n")

    for i, file in enumerate(files, 1):
        path = Path(file)
        if not path.exists():
            print(f"❌ [{i}/{total}] Missing: {path}")
            unrepairable.append(str(path))
            continue

        print(f"🔄 [{i}/{total}] Repairing: {path}")
        success = try_repair(path)

        if not success:
            print(f"⚠️   Failed to repair: {path}")
            unrepairable.append(str(path))

    if unrepairable:
        with open(UNREPAIRABLE_LOG, "w") as f:
            f.write("\n".join(unrepairable))
        print(f"\n⚠️  {len(unrepairable)} files could not be repaired.")
        print(f"📄 See: {UNREPAIRABLE_LOG}")
    else:
        print("\n✅ All broken files repaired successfully!")


if __name__ == "__main__":
    main()
