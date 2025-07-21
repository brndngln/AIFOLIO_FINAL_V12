import os
import sys

# List of common standard library modules that might be shadowed
standard_modules = [
    "subprocess",
    "types",
    "warnings",
    "os",
    "sys",
    "re",
    "enum",
    "requests",
    "logging",
    "json",
    "time",
    "datetime",
    "math",
    "random",
    "collections",
    "string",
    "http",
]


def detect_shadowed_modules():
    shadowed_files = []
    for module in standard_modules:
        try:
            mod = importlib.import_module(module)
            if hasattr(mod, "__file__"):
                mod_path = mod.__file__
                if (
                    mod_path
                    and os.path.basename(mod_path).startswith(module + ".py")
                    and os.path.dirname(mod_path) == os.getcwd()
                ):
                    shadowed_files.append((module, mod_path))
        except ImportError:
            continue  # Skip if module import fails
    return shadowed_files


def fix_shadowing(shadowed_files):
    fixed = []
    for module, path in shadowed_files:
        backup_name = f"{module}_backup.py"
        if os.path.exists(path):
            os.rename(path, backup_name)
            fixed.append(f"Renamed {path} to {backup_name}")
    return fixed


if __name__ == "__main__":
    print(f"Using Python {sys.version}")
    print("Detecting and fixing shadowing issues...\n")

    shadowed_files = detect_shadowed_modules()
    if shadowed_files:
        print("Found shadowed modules:")
        for module, path in shadowed_files:
            print(f"  - {module} at {path}")
        print("\nFixing by renaming conflicting files:")
        fixes = fix_shadowing(shadowed_files)
        for fix in fixes:
            print(fix)
        print(
            "\nShadowing fixed! Please re-run your scripts (e.g., python3 vault_manager.py)."
        )
    else:
        print("No shadowing issues detected. You're good to go!")
