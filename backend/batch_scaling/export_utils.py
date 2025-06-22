import os
import csv
from fastapi.responses import FileResponse
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
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return path

@safe_ai_guarded
def export_pdf(filename, template_name, context, folder='pdf'):
    env = Environment(loader=FileSystemLoader('./backend/batch_scaling/templates'))
    template = env.get_template(template_name)
    html_out = template.render(**context)
    pdf_path = os.path.join(EXPORT_PATHS[folder], filename)
    HTML(string=html_out).write_pdf(pdf_path)
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
