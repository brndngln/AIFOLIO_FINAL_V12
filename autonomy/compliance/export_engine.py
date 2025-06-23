import csv
import os
import json
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

"""
AIFOLIO Export Engine
- Fully static, deterministic, SAFE AI compliant
- No live event bus calls; all logic is static
- Audit-logs all export events
- GDPR/CCPA compliant, owner controlled
"""
import os
import json
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

EXPORT_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../analytics/export_log.json')

def _audit_export(event, details=None):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'event': event,
        'details': details or {}
    }
    if os.path.exists(EXPORT_LOG_PATH):
        with open(EXPORT_LOG_PATH, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(EXPORT_LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)

def export_to_pdf(data: dict, filename: str, owner_override=None):
    """
    Static SAFE AI PDF export. Owner can override export content. Audit-logged.
    """
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        y = 750
        export_data = owner_override if owner_override is not None else data
        for k, v in export_data.items():
            c.drawString(50, y, f"{k}: {v}")
            y -= 20
        c.save()
        _audit_export('EXPORT_PDF', {'filename': filename, 'data': export_data})
        return filename
    except Exception as e:
        _audit_export('EXPORT_PDF_FAILED', {'filename': filename, 'error': str(e), 'data': data})
        raise

def export_to_csv(data: dict, filename: str, owner_override=None):
    """
    Static SAFE AI CSV export. Owner can override export content. Audit-logged.
    """
    try:
        export_data = owner_override if owner_override is not None else data
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(export_data.keys())
            writer.writerow(export_data.values())
        _audit_export('EXPORT_CSV', {'filename': filename, 'data': export_data})
        return filename
    except Exception as e:
        _audit_export('EXPORT_CSV_FAILED', {'filename': filename, 'error': str(e), 'data': data})
        raise

def export_to_xbrl(financial_data: dict, owner_override=None):
    """
    Static SAFE AI XBRL export. Owner can override export content. Audit-logged.
    """
    path = tempfile.mktemp(suffix=".xbrl")
    try:
        export_data = owner_override if owner_override is not None else financial_data
        with open(path, "w") as f:
            f.write("<!-- XBRL export stub: integrate with arelle for real use -->\n")
            f.write(json.dumps(export_data, indent=2))
        _audit_export('EXPORT_XBRL', {'filename': path, 'data': export_data})
        return path
    except Exception as e:
        _audit_export('EXPORT_XBRL_FAILED', {'filename': path, 'error': str(e), 'data': financial_data})
        raise
    except Exception as e:
        event_bus.dispatch_event(EVENT_EXPORT_FAILED, {
            'export_type': 'xbrl',
            'filename': path,
            'error': str(e),
            'data': financial_data
        })
        raise
