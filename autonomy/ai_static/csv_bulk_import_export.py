"""
AIFOLIO™ SAFE AI MODULE: CSV Bulk Import/Export
- Static, non-sentient
- Imports/exports vault data in CSV format with full logging
- No autonomous data transformation or adaptive import
"""
import csv
import logging

LOG_PATH = "../../distribution/legal_exports/csv_import_export_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def import_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        logging.info(f"Imported {len(data)} records from {path}")
        return data

def export_csv(path, data, fieldnames):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        logging.info(f"Exported {len(data)} records to {path}")
