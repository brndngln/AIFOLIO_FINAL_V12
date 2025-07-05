"""
OMNIELITE Audit Trail Export & Search Tool
OWNER-controlled, static CLI for searching/exporting audit logs.
No adaptive/sentient logic. Exports are SHA256 signed.
"""
import os
import json
import hashlib
from glob import glob

EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "audit", "exports")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "compliance_reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def search_audit(field=None, value=None):
    results = []
    for f in glob(os.path.join(EXPORTS_DIR, "*.json")):
        with open(f) as fp:
            data = json.load(fp)
            for entry in data if isinstance(data, list) else []:
                if field is None or (str(entry.get(field, "")) == str(value)):
                    results.append(entry)
    return results


def export_results(results, filename):
    out_path = os.path.join(REPORTS_DIR, filename)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    # SHA256 hash
    hashval = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()
    with open(out_path + ".sha256", "w") as f:
        f.write(hashval)
    print(f"Exported {len(results)} entries to {out_path} (SHA256: {hashval})")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="OMNIELITE Audit Exporter")
    parser.add_argument("--field", type=str, help="Field to filter by")
    parser.add_argument("--value", type=str, help="Value to match for field")
    parser.add_argument(
        "--output", type=str, default="audit_export.json", help="Output filename"
    )
    args = parser.parse_args()
    results = search_audit(args.field, args.value)
    export_results(results, args.output)


if __name__ == "__main__":
    main()
