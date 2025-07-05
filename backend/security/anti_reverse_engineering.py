"""
AIFOLIO Anti-Reverse Engineering
Static, deterministic, SAFE AI-compliant watermarking for PDF assets.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_WATERMARK = "AIFOLIO-SECURE-WATERMARK-2025"


def apply_watermark(pdf_path: str) -> str:
    # Simulate watermarking by appending static watermark metadata
    watermarked_pdf_path = pdf_path.replace(".pdf", "_wm.pdf")
    with open(pdf_path, "rb") as f:
        content = f.read()
    with open(watermarked_pdf_path, "wb") as f:
        f.write(content)
        f.write(b"\n" + STATIC_WATERMARK.encode())
    logger.info(f"PDF watermarked: {watermarked_pdf_path}")
    return watermarked_pdf_path
