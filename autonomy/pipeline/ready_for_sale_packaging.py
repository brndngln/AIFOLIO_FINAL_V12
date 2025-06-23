import os
import json
import datetime
from PyPDF2 import PdfReader

PACKAGING_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ready_for_sale_packaging_log.jsonl'))
os.makedirs(os.path.dirname(PACKAGING_LOG), exist_ok=True)

# --- Package Integrity Checker ---
import re

def slugify_filename(title, prefix="AIFOLIO"):  # Helper for filename standardization
    # Remove non-alphanumeric, replace spaces with _, uppercase
    base = re.sub(r'[^A-Za-z0-9 ]+', '', title)
    base = '_'.join(base.strip().split())
    return f"{prefix}_{base}.pdf"

def is_garbage_filename(filename):
    # Block files with patterns like Final, Copy, etc.
    return bool(re.search(r'(final|copy|draft|temp|untitled|test)', filename, re.IGNORECASE))

def check_pdf_compliance(pdf_path):
    # Check for blank pages, watermarks, forbidden words, file size
    try:
        reader = PdfReader(pdf_path)
        blank_pages = 0
        forbidden_words = ['SAMPLE', 'WATERMARK', 'DRAFT']
        forbidden_found = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ''
            if not text.strip():
                blank_pages += 1
            for word in forbidden_words:
                if word in text.upper():
                    forbidden_found.append((i, word))
        file_size = os.path.getsize(pdf_path)
        return {
            'blank_pages': blank_pages,
            'forbidden_found': forbidden_found,
            'file_size': file_size,
            'valid': blank_pages == 0 and not forbidden_found and file_size > 1024
        }
    except Exception as e:
        return {'error': str(e), 'valid': False}

def check_package_integrity(files, metadata_path=None, allow_manual_override=False):
    missing = [f for f in files if not os.path.exists(f)]
    pdfs = [f for f in files if f.lower().endswith('.pdf') and os.path.exists(f)]
    pdf_valid = []
    compliance = []
    standardized_names = []
    manual_override_needed = False
    for pdf in pdfs:
        # Filename standardization
        fname = os.path.basename(pdf)
        if is_garbage_filename(fname):
            # Try to auto-rename
            title = None
            if metadata_path and os.path.exists(metadata_path):
                with open(metadata_path) as f:
                    meta = json.load(f)
                    title = meta.get('title')
            if title:
                new_name = slugify_filename(title)
                new_path = os.path.join(os.path.dirname(pdf), new_name)
                os.rename(pdf, new_path)
                standardized_names.append(new_path)
                # Update metadata
                if metadata_path and os.path.exists(metadata_path):
                    with open(metadata_path) as f:
                        meta = json.load(f)
                    meta['pdf_filename'] = new_name
                    with open(metadata_path, 'w') as f:
                        json.dump(meta, f, indent=2)
            else:
                manual_override_needed = True
                standardized_names.append(pdf)
        else:
            standardized_names.append(pdf)
        # Compliance check
        compliance.append(check_pdf_compliance(pdf))
        pdf_valid.append(compliance[-1]['valid'])
    result = {
        'missing': missing,
        'pdf_valid': pdf_valid,
        'compliance': compliance,
        'standardized_names': standardized_names,
        'manual_override_needed': manual_override_needed
    }
    # Log result (JSONL for dashboard)
    log_entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'event': 'pdf_compliance_check',
        'files': files,
        'metadata_path': metadata_path,
        'result': result,
        'status': (
            'manual_override_needed' if manual_override_needed else (
                'compliance_failed' if not all(pdf_valid) else 'success'
            )
        ),
        'error': None
    }
    if manual_override_needed:
        log_entry['error'] = 'Manual override required for filename standardization.'
    elif not all(pdf_valid):
        log_entry['error'] = 'PDF compliance failed.'
    with open(PACKAGING_LOG, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    return result


# --- AI-generated Final Checklist ---
def generate_final_checklist(product_id, files, metadata_path=None, allow_manual_override=False):
    integrity = check_package_integrity(files, metadata_path, allow_manual_override)
    checklist = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'product_id': product_id,
        'files_checked': files,
        'integrity': integrity,
        'human_preview_required': integrity.get('manual_override_needed', False)
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
