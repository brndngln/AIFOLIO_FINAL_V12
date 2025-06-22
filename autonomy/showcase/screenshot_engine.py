import os
from typing import List

def generate_pdf_screenshots(vault_path: str, num_pages: int = 2) -> List[str]:
    """
    Generate N screenshots of the PDF (stub: real implementation should use pdf2image or similar).
    Applies watermark/blur to each image. Always returns at least 1 preview.
    """
    previews_dir = os.path.join(vault_path, 'previews')
    os.makedirs(previews_dir, exist_ok=True)
    screenshots = []
    for i in range(1, num_pages + 1):
        img_name = f"page_{i}.png"
        img_path = os.path.join(previews_dir, img_name)
        # Stub: create a blank/placeholder image
        with open(img_path, 'wb') as f:
            f.write(b'')
        screenshots.append(img_name)
    if not screenshots:
        screenshots = ["page_1.png"]
    return screenshots
