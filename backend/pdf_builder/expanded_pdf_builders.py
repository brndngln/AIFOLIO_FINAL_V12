import os
from typing import Dict, Any, List
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
from backend.utils.safe_ai_utils import safe_ai_guarded

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), '../typesetter/templates')
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

def _render_and_save_pdf(filename: str, content: str, extra_context: Dict[str, Any] = None) -> str:
    os.makedirs("vaults", exist_ok=True)
    template = env.get_template('vault_template.html')
    html_content = template.render(content=content, **(extra_context or {}))
    pdf_path = f"vaults/{filename}.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    logger.info(f"PDF generated successfully: {pdf_path}")
    return pdf_path

# 1️⃣ Niche Product PDF Generator
@safe_ai_guarded
def build_niche_product_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>{data.get('catalog_title', 'Product Catalog')}</h1>
    <ul>{''.join([f'<li>{p}</li>' for p in data.get('products', [])])}</ul>
    <h2>Sales Sheet</h2><p>{data.get('sales_sheet', '')}</p>
    <h2>Buyer’s Guide</h2><p>{data.get('buyers_guide', '')}</p>
    <h2>Ingredient Sheet</h2><p>{data.get('ingredient_sheet', '')}</p>
    <h2>Printable 1-Pager</h2><p>{data.get('one_pager', '')}</p>
    """
    return _render_and_save_pdf(data.get('catalog_title', 'Product_Catalog'), content)

# 2️⃣ Affiliate Promo Pack PDF
@safe_ai_guarded
def build_affiliate_promo_pack_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>Affiliate Promo Pack: {data.get('product_name', '')}</h1>
    <h2>Product Descriptions</h2><p>{data.get('product_descriptions', '')}</p>
    <h2>Promo Headlines</h2><ul>{''.join([f'<li>{h}</li>' for h in data.get('promo_headlines', [])])}</ul>
    <h2>Discount Codes</h2><ul>{''.join([f'<li>{c}</li>' for c in data.get('discount_codes', [])])}</ul>
    <h2>Swipe Email Templates</h2><p>{data.get('email_templates', '')}</p>
    <h2>Banner Image Previews</h2><ul>{''.join([f'<li>{b}</li>' for b in data.get('banner_images', [])])}</ul>
    """
    return _render_and_save_pdf(f"Affiliate_Promo_{data.get('product_name', 'Pack')}", content)

# 3️⃣ Social Media Content Pack PDF
@safe_ai_guarded
def build_social_media_content_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>Social Media Content Pack</h1>
    <h2>Captions</h2><ul>{''.join([f'<li>{c}</li>' for c in data.get('captions', [])])}</ul>
    <h2>Hashtags</h2><ul>{''.join([f'<li>{h}</li>' for h in data.get('hashtags', [])])}</ul>
    <h2>Stories Ideas</h2><ul>{''.join([f'<li>{s}</li>' for s in data.get('stories_ideas', [])])}</ul>
    <h2>CTA Blurbs</h2><ul>{''.join([f'<li>{cta}</li>' for cta in data.get('cta_blurbs', [])])}</ul>
    <h2>Image Suggestions</h2><ul>{''.join([f'<li>{img}</li>' for img in data.get('image_suggestions', [])])}</ul>
    """
    return _render_and_save_pdf("Social_Media_Content_Pack", content)

# 4️⃣ AI Market Trends Report PDF
@safe_ai_guarded
def build_market_trends_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>AI Market Trends Report</h1>
    <h2>Top Product Trends</h2><ul>{''.join([f'<li>{t}</li>' for t in data.get('product_trends', [])])}</ul>
    <h2>Niche Keyword Trends</h2><ul>{''.join([f'<li>{k}</li>' for k in data.get('keyword_trends', [])])}</ul>
    <h2>Competitor Insights</h2><p>{data.get('competitor_insights', '')}</p>
    <h2>Reporting Period</h2><p>{data.get('report_period', '')}</p>
    """
    return _render_and_save_pdf("Market_Trends_Report", content)

# 5️⃣ AI Revenue & Conversion Report PDF
@safe_ai_guarded
def build_revenue_conversion_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>AI Revenue & Conversion Report</h1>
    <h2>Revenue Trends</h2><ul>{''.join([f'<li>{r}</li>' for r in data.get('revenue_trends', [])])}</ul>
    <h2>Conversion Rates</h2><ul>{''.join([f'<li>{c}</li>' for c in data.get('conversion_rates', [])])}</ul>
    <h2>Top-Selling Products</h2><ul>{''.join([f'<li>{p}</li>' for p in data.get('top_products', [])])}</ul>
    <h2>Affiliate Performance</h2><ul>{''.join([f'<li>{a}</li>' for a in data.get('affiliate_performance', [])])}</ul>
    <h2>Funnel Performance</h2><ul>{''.join([f'<li>{f}</li>' for f in data.get('funnel_performance', [])])}</ul>
    """
    return _render_and_save_pdf("Revenue_Conversion_Report", content)

# 6️⃣ Customer Welcome Pack PDF
@safe_ai_guarded
def build_customer_welcome_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>Welcome to {data.get('brand', 'Our Brand')}</h1>
    <h2>Welcome Letter</h2><p>{data.get('welcome_letter', '')}</p>
    <h2>Brand Story</h2><p>{data.get('brand_story', '')}</p>
    <h2>Tips / How to Use Products</h2><ul>{''.join([f'<li>{tip}</li>' for tip in data.get('tips', [])])}</ul>
    <h2>Discounts / Next Steps</h2><p>{data.get('discounts', '')}</p>
    """
    return _render_and_save_pdf("Customer_Welcome_Pack", content)

# 7️⃣ Niche Authority eBook Generator
@safe_ai_guarded
def build_niche_authority_ebook(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>{data.get('ebook_title', 'Niche Authority eBook')}</h1>
    <h2>Top Tips / Education</h2><ul>{''.join([f'<li>{tip}</li>' for tip in data.get('top_tips', [])])}</ul>
    <h2>Product Mentions</h2><ul>{''.join([f'<li>{m}</li>' for m in data.get('product_mentions', [])])}</ul>
    <h2>SEO Optimized</h2><p>{data.get('seo_notes', '')}</p>
    <h2>Lead Magnet Ready</h2><p>{data.get('lead_magnet', '')}</p>
    """
    return _render_and_save_pdf(data.get('ebook_title', 'Niche_Authority_eBook'), content)

# 8️⃣ Email Funnel Blueprint PDF
@safe_ai_guarded
def build_email_funnel_blueprint_pdf(data: Dict[str, Any]) -> str:
    content = f"""
    <h1>Email Funnel Blueprint</h1>
    <h2>Suggested Email Sequences</h2><ul>{''.join([f'<li>{seq}</li>' for seq in data.get('email_sequences', [])])}</ul>
    <h2>Timings</h2><ul>{''.join([f'<li>{t}</li>' for t in data.get('timings', [])])}</ul>
    <h2>Example Content</h2><p>{data.get('example_content', '')}</p>
    <h2>Personalization Tips</h2><ul>{''.join([f'<li>{tip}</li>' for tip in data.get('personalization_tips', [])])}</ul>
    """
    return _render_and_save_pdf("Email_Funnel_Blueprint", content)
