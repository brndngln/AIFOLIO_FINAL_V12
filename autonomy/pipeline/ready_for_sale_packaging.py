import os
import json
import datetime
from PyPDF2 import PdfReader

PACKAGING_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ready_for_sale_packaging_log.jsonl'))
os.makedirs(os.path.dirname(PACKAGING_LOG), exist_ok=True)

# --- Package Integrity Checker ---
def check_package_integrity(files):
    missing = [f for f in files if not os.path.exists(f)]
    pdfs = [f for f in files if f.lower().endswith('.pdf') and os.path.exists(f)]
    pdf_valid = []
    for pdf in pdfs:
        try:
            reader = PdfReader(pdf)
            pdf_valid.append(True)
        except Exception:
            pdf_valid.append(False)
    return {'missing': missing, 'pdf_valid': pdf_valid}

# --- AI-generated Final Checklist ---
def generate_final_checklist(product_id, files):
    integrity = check_package_integrity(files)
    checklist = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'product_id': product_id,
        'files_checked': files,
        'integrity': integrity,
        'human_preview_required': True
    }
    with open(PACKAGING_LOG, 'a') as f:
        f.write(json.dumps(checklist) + '\n')
    return checklist

# --- PDF Visual Preview (stub) ---
def pdf_visual_preview(pdf_path):
    # Stub: Just returns first page text for preview
    if not os.path.exists(pdf_path):
        return None
    try:
        reader = PdfReader(pdf_path)
        return reader.pages[0].extract_text()
    except Exception:
        return None

if __name__ == "__main__":
    files = ['sample.pdf', 'cover.jpg']
    print(json.dumps(check_package_integrity(files), indent=2))
    print(json.dumps(generate_final_checklist('prod_1', files), indent=2))
