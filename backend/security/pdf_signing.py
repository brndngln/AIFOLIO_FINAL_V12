"""
AIFOLIO Signed PDF Outputs
Static, deterministic, SAFE AI-compliant PDF signing logic.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_SIGNATURE = "AIFOLIO-OWNER-SIGNED-2025"


def sign_pdf(pdf_path: str) -> str:
    # Simulate signing by appending static signature metadata
    signed_pdf_path = pdf_path.replace('.pdf', '_signed.pdf')
    with open(pdf_path, 'rb') as f:
        content = f.read()
    with open(signed_pdf_path, 'wb') as f:
        f.write(content)
        f.write(b"\n" + STATIC_SIGNATURE.encode())
    logger.info(f"PDF signed: {signed_pdf_path}")
    return signed_pdf_path
