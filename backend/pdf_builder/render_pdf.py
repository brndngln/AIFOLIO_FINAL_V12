from weasyprint import HTML
import os
import logging
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def build_pdf(vault_data: Dict[str, Any], compliance_report: Dict[str, Any]) -> str:
    """Build a PDF from vault data and compliance report using Jinja2 and vault_template.html."""
    try:
        logger.info(f"Building PDF for vault: {vault_data['title']}")

        # Create directories if they don't exist
        os.makedirs("vaults", exist_ok=True)

        # Setup Jinja2 environment to load the template
        template_dir = os.path.join(os.path.dirname(__file__), '../typesetter/templates')
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('vault_template.html')

        # Prepare main content (e.g., chapters, etc.)
        content = f"""
        <h1>{vault_data['title']}</h1>
        <p>{vault_data['description']}</p>
        <h2>Table of Contents</h2>
        <ul>
            {''.join([f'<li>{ch}</li>' for ch in vault_data.get('chapters', [])])}
        </ul>
        <div class='cta'><p>{vault_data.get('cta', '')}</p></div>
        """

        # AI SAFETY CHECK
        if not anti_sentience_guard(content, user=None, action='render_pdf'):
            raise Exception('AI safety violation: Unsafe sentience/agency patterns detected in PDF content.')

        # Render the template with compliance_report and content
        html_content = template.render(
            compliance_report=compliance_report,
            content=content
        )

        # AI SAFETY CHECK
        if not anti_sentience_guard(html_content, user=None, action='render_pdf'):
            raise Exception('AI safety violation: Unsafe sentience/agency patterns detected in PDF content.')

        # Generate PDF
        pdf_path = f"vaults/{vault_data['title']}.pdf"
        HTML(string=html_content).write_pdf(pdf_path)
        logger.info(f"PDF generated successfully: {pdf_path}")
        return pdf_path
    except Exception as e:
        logger.error(f"Error building PDF: {str(e)}")
        raise
            
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
