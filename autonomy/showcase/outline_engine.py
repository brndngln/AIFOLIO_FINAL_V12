import os
import json
import re
from typing import List

def extract_outline_from_pdf_or_md(vault_path: str) -> List[str]:
    """
    Extract a structured outline from a PDF or Markdown file in the vault.
    Returns a list of up to 10 top-level outline items.
    """
    outline = []
    # Try Markdown first
    md_path = os.path.join(vault_path, 'vault.md')
    pdf_path = os.path.join(vault_path, 'vault.pdf')
    if os.path.exists(md_path):
        with open(md_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if re.match(r'^(#|\d+\.|\*\*)', line.strip()):
                clean = re.sub(r'[#*\d. ]+', '', line).strip()
                if clean:
                    outline.append(clean)
            if len(outline) >= 10:
                break
    elif os.path.exists(pdf_path):
        # Placeholder: PDF parsing stub (use PyPDF2 or pdfminer for real extraction)
        outline = [f"Section {i+1}" for i in range(5)]
    if len(outline) < 5:
        outline += [f"Section {i+1}" for i in range(len(outline), 5)]
    return outline[:10]


def save_outline(vault_path: str, outline: List[str]):
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r') as f:
            preview = json.load(f)
    else:
        preview = {}
    preview['outline'] = outline
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
