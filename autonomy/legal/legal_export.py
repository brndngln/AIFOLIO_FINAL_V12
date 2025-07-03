import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from autonomy.legal.policy_translator import translate_policy

POLICY_FILES = [
    ("terms_of_service", "terms_of_service.md"),
    ("refund_policy", "refund_policy.md"),
    ("privacy_policy", "privacy_policy.md")
]

EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/'))
os.makedirs(EXPORT_DIR, exist_ok=True)

def get_policy_markdown(policy_name: str) -> str:
    for key, fname in POLICY_FILES:
        if key == policy_name:
            path = os.path.join(os.path.dirname(__file__), fname)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return f.read()
    return ""

def export_all_policies_as_pdf(output_path: str, language: str = "en"):
    """
    Export all policies as PDF to the output_path. Supports multi-language export.
    """
    for key, fname in POLICY_FILES:
        md = get_policy_markdown(key)
        if not md:
            continue
        if language != "en":
            md = translate_policy(key, language)
        pdf_path = os.path.join(output_path, f"{key}_{language}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        y = 750
        for line in md.split('\n'):
            c.drawString(50, y, line)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
    return True
