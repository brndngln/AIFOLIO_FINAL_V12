pt = None  # TODO: Define pt
import os
import subprocess
import sys

print(f"Using Python {sys.version}")


def check_files():
    key_files = ["vault_manager.py", "trainer.py", "tokenization_bert.py"]
    for file in key_files:
        if os.path.exists(file):
            print(f"Found {file}")
        else:
            print(f"Missing {file}")


def run_tests():
    scripts = ["python3 vault_manager.py", "python3 trainer.py"]
    for script in scripts:
        result = subprocess.call(script, shell=True)
        if result == 0:
            print(f"Running {script}: Success")
        else:
            print(f"Running {script}: Failed with exit code {result}")


if __name__ == "__main__":
    print("Checking setup...")
    check_files()
    print("Running basic tests...")
    run_tests()
    print("Setup check complete!")
