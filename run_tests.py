#!/usr/bin/env python3
"""Test runner script for AIFOLIO test suite."""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all", coverage=True, verbose=True):
    """Run tests with specified options."""
    cmd = ["python", "-m", "pytest"]
    
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "performance":
        cmd.extend(["-m", "performance"])
    
    if coverage:
        cmd.extend(["--cov=src", "--cov=core", "--cov-report=html", "--cov-report=term-missing"])
    
    if verbose:
        cmd.append("-v")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run AIFOLIO tests")
    parser.add_argument("--type", choices=["all", "unit", "integration", "performance"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet
    )
    
    sys.exit(exit_code)
