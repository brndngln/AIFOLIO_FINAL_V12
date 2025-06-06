from weasyprint import HTML
import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def build_pdf(vault_data: Dict[str, Any]) -> str:
    """Build a PDF from vault data."""
    try:
        logger.info(f"Building PDF for vault: {vault_data['title']}")
        
        # Create directories if they don't exist
        os.makedirs("vaults", exist_ok=True)
        
        # Generate HTML content with enhanced formatting
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 30px;
                }}
                h2 {{
                    color: #3498db;
                    margin-top: 30px;
                    margin-bottom: 15px;
                }}
                p {{
                    margin-bottom: 15px;
                }}
                ul {{
                    margin-left: 20px;
                }}
                li {{
                    margin-bottom: 10px;
                }}
                .cta {{
                    text-align: center;
                    margin-top: 30px;
                    font-weight: bold;
                    color: #e74c3c;
                    font-size: 1.2em;
                }}
            </style>
        </head>
        <body>
            <h1>{vault_data['title']}</h1>
            <p>{vault_data['description']}</p>
            
            <h2>Table of Contents</h2>
            <ul>
                {''.join([f'<li>{ch}</li>' for ch in vault_data['chapters']])}
            </ul>
            
            <div class="cta">
                <p>{vault_data['cta']}</p>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF
        pdf_path = f"vaults/{vault_data['title']}.pdf"
        HTML(string=html_content).write_pdf(pdf_path)
        logger.info(f"PDF generated successfully: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error building PDF: {str(e)}")
        raise
