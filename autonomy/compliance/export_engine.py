import csv
import os
import json
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from autonomy.pipeline import event_bus
from autonomy.pipeline.event_definitions import EVENT_EXPORT_FAILED

try:
    import arelle
except ImportError:
    arelle = None

# --- PDF Export ---
def export_to_pdf(data: dict, filename: str):
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        y = 750
        for k, v in data.items():
            c.drawString(50, y, f"{k}: {v}")
            y -= 20
        c.save()
        return filename
    except Exception as e:
        # Dispatch export_failed event
        event_bus.dispatch_event(EVENT_EXPORT_FAILED, {
            'export_type': 'pdf',
            'filename': filename,
            'error': str(e),
            'data': data
        })
        raise

# --- CSV Export ---
def export_to_csv(data: dict, filename: str):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        return filename
    except Exception as e:
        event_bus.dispatch_event(EVENT_EXPORT_FAILED, {
            'export_type': 'csv',
            'filename': filename,
            'error': str(e),
            'data': data
        })
        raise

# --- XBRL Export (stub: use arelle for real) ---
def export_to_xbrl(financial_data: dict):
    path = tempfile.mktemp(suffix=".xbrl")
    try:
        with open(path, "w") as f:
            f.write("<!-- XBRL export stub: integrate with arelle for real use -->\n")
            f.write(json.dumps(financial_data, indent=2))
        return path
    except Exception as e:
        event_bus.dispatch_event(EVENT_EXPORT_FAILED, {
            'export_type': 'xbrl',
            'filename': path,
            'error': str(e),
            'data': financial_data
        })
        raise
