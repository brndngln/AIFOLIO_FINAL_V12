import os
import csv
<<<<<<< HEAD
from fastapi.responses import FileResponse
=======
>>>>>>> omni_repair_backup_20250704_1335
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from backend.utils.safe_ai_utils import safe_ai_guarded

EXPORT_PATHS = {
    'pdf': os.path.abspath('./exports/pdf/'),
    'csv': os.path.abspath('./exports/csv/'),
    'partner_certification': os.path.abspath('./exports/partner_certification/'),
    'public_reports': os.path.abspath('./exports/public_reports/')
}

for path in EXPORT_PATHS.values():
    os.makedirs(path, exist_ok=True)

def export_csv(filename, data, fieldnames, folder='csv'):
    path = os.path.join(EXPORT_PATHS[folder], filename)
    try:
        with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        log_export_failure('export_csv', 'system', {'file': path, 'error': str(e)})
        raise
    return path

@safe_ai_guarded
def export_pdf(filename, template_name, context, folder='pdf'):
    env = Environment(loader=FileSystemLoader('./backend/batch_scaling/templates'))
    template = env.get_template(template_name)
    html_out = template.render(**context)
    pdf_path = os.path.join(EXPORT_PATHS[folder], filename)
    try:
        HTML(string=html_out).write_pdf(pdf_path)
    except Exception as e:
        log_export_failure('export_pdf', 'system', {'file': pdf_path, 'error': str(e)})
        raise
    return pdf_path

# Logging utility
def log_export(action, user, details):
    log_path = './analytics/ai_safety_log.jsonl'
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'user': user,
        'details': details
    }
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(str(entry) + '\n')

def log_export_failure(action, user, details):
    os.makedirs('./logs', exist_ok=True)
    log_path = './logs/export_failures.json'
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'user': user,
        'details': details
    }
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                log = f.read().strip()
                existing = []
                if log:
                    import json
                    existing = json.loads(log)
        else:
            existing = []
    except Exception:
        existing = []
    existing.append(entry)
    import json
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(existing, indent=2))

def get_last_updated(filename, folder='pdf'):
    path = os.path.join(EXPORT_PATHS[folder], filename)
    if not os.path.exists(path):
        return None
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %I:%M %p')
