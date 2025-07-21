import os
import sys

# List of standard library modules to check for shadowing
standard_modules = ["subprocess", "types", "warnings", "os", "re", "enum"]


def check_shadowed_modules():
    issues = []
    for module in standard_modules:
        try:
            mod = importlib.import_module(module)
            # Check if the module is a built-in (no __file__) or a file-based module
            if module == "sys" or not hasattr(mod, "__file__"):
                issues.append(
                    f"{module} is a built-in module, no shadowing check needed."
                )
            else:
                mod_path = mod.__file__
                if (
                    mod_path
                    and os.path.basename(mod_path).startswith(module + ".py")
                    and os.path.dirname(mod_path) == os.getcwd()
                ):
                    issues.append(f"Shadowed {module} found at {mod_path} - rename it!")
                else:
                    issues.append(f"{module} is loading correctly from {mod_path}")
        except ImportError as e:
            issues.append(f"Failed to import {module}: {str(e)}")
    return issues


def check_key_files():
    key_files = ["vault_manager.py", "trainer.py", "tokenization_bert.py"]
    file_issues = []
    for file in key_files:
        if not os.path.exists(file):
            file_issues.append(f"Missing {file}")
    return file_issues


def run_test_scripts():
    test_issues = []
    scripts = ["python3 vault_manager.py", "python3 trainer.py"]
    for script in scripts:
        try:
            result = os.system(script)
            if result != 0:
                test_issues.append(f"Running {script} failed with exit code {result}")
            else:
                test_issues.append(f"Running {script} succeeded")
        except Exception as e:
            test_issues.append(f"Error running {script}: {str(e)}")
    return test_issues


if __name__ == "__main__":
    print(f"Using Python {sys.version}")
    print("Running diagnostic check...\n")

    print("Checking for shadowed modules:")
    module_issues = check_shadowed_modules()
    for issue in module_issues:
        print(issue)

    print("\nChecking key files:")
    file_issues = check_key_files()
    for issue in file_issues:
        print(issue)

    print("\nTesting key scripts:")
    test_issues = run_test_scripts()
    for issue in test_issues:
        print(issue)

    print("\nDiagnostic complete!")
    if any(
        issue.startswith("Failed")
        or issue.startswith("Missing")
        or issue.startswith("Shadowed")
        for issue in module_issues + file_issues + test_issues
    ):
        print(
            "Issues found—review and rename shadowed files or fix missing dependencies."
        )
    else:
        print("No issues detected! You're ready to proceed.")
