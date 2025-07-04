"""
OMNIELITE SAFE AI Compliance Regression Test Runner
Runs all tests, outputs results to compliance_report.json, and integrates with the dashboard.
No adaptive/sentient logic.
"""
import os
import json
import subprocess
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'compliance_reports')
os.makedirs(REPORTS_DIR, exist_ok=True)


def run_tests():
    result = subprocess.run(
        ['pytest', '--maxfail=10', '--disable-warnings', '-q', '--tb=short'],
        capture_output=True, text=True
    )
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }

def main():
    results = run_tests()
    report = {
        'timestamp': datetime.now().isoformat(),
        'results': results
    }
    with open(os.path.join(REPORTS_DIR, 'compliance_report.json'), 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Compliance test suite run. Results saved to {REPORTS_DIR}/compliance_report.json")

if __name__ == '__main__':
    main()
