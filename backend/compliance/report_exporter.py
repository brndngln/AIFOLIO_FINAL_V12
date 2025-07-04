import json
import csv
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import base64

VIOLATION_LOG = Path(__file__).parent.parent / 'logs' / 'compliance_violations.json'
REPORT_DIR = Path(__file__).parent.parent / 'exports'
REPORT_DIR.mkdir(parents=True, exist_ok=True)

BRAND_WATERMARK = 'AIFOLIO™ Compliance Engine vX.ELITE — Audit-Ready'

# Mask reviewer IDs for privacy

def mask_reviewer_id(rid):
    if not rid: return ''
    return rid[:2] + '***' + rid[-2:]

def export_json(doc_id=None):
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    if doc_id:
        violations = [v for v in violations if v['doc_id'] == doc_id]
    out = {
        'exported_at': datetime.utcnow().isoformat(),
        'brand': BRAND_WATERMARK,
        'violations': violations
    }
    fname = REPORT_DIR / f'compliance_report_{doc_id or "all"}_{int(datetime.utcnow().timestamp())}.json'
    with open(fname, 'w') as f:
        json.dump(out, f, indent=2)
    return str(fname)

def export_csv(doc_id=None):
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    if doc_id:
        violations = [v for v in violations if v['doc_id'] == doc_id]
    fname = REPORT_DIR / f'compliance_report_{doc_id or "all"}_{int(datetime.utcnow().timestamp())}.csv'
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['DocID', 'Desc', 'Law', 'Severity', 'Status', 'SLA', 'Reviewer', 'Fix History', 'Final'])
        for v in violations:
            writer.writerow([
                v.get('doc_id'),
                v.get('description'),
                v.get('law'),
                v.get('severity'),
                v.get('status'),
                v.get('sla_status'),
                mask_reviewer_id(v.get('assigned_reviewer')),
                json.dumps(v.get('fix_history', [])),
                'PASS' if v.get('status') == 'resolved' else 'FAIL'
            ])
    return str(fname)

def export_pdf(doc_id=None):
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    if doc_id:
        violations = [v for v in violations if v['doc_id'] == doc_id]
    fname = REPORT_DIR / f'compliance_report_{doc_id or "all"}_{int(datetime.utcnow().timestamp())}.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, BRAND_WATERMARK, ln=1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f'Exported: {datetime.utcnow().isoformat()}', ln=1)
    for v in violations:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'DocID: {v.get("doc_id")}', ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, f"Desc: {v.get('description')}\nLaw: {v.get('law')}\nSeverity: {v.get('severity')}\nStatus: {v.get('status')}\nSLA: {v.get('sla_status')}\nReviewer: {mask_reviewer_id(v.get('assigned_reviewer'))}\nFix History: {json.dumps(v.get('fix_history', []))}\nFinal: {'PASS' if v.get('status') == 'resolved' else 'FAIL'}", border=1)
        pdf.ln(2)
    pdf.output(str(fname))
    # Optionally encode as base64 for API download
    with open(fname, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return {'file': str(fname), 'base64': b64}
