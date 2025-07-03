import pandas as pd
import os
import datetime
import json

CSV_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/csv_import_export_log.jsonl'))
os.makedirs(os.path.dirname(CSV_LOG), exist_ok=True)

# --- CSV Bulk Import/Export ---
def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'action': 'export',
        'filename': filename,
        'row_count': len(df)
    }
    with open(CSV_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return filename

def import_from_csv(filename):
    df = pd.read_csv(filename)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'action': 'import',
        'filename': filename,
        'row_count': len(df)
    }
    with open(CSV_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return df.to_dict(orient='records')

if __name__ == "__main__":
    test_data = [{"vault": "v1", "amount": 100}, {"vault": "v2", "amount": 200}]
    export_to_csv(test_data, 'test_export.csv')
    print(import_from_csv('test_export.csv'))
