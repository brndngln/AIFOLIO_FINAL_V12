import os
import json
from .outline_engine import extract_outline_from_pdf_or_md, save_outline
from .screenshot_engine import generate_pdf_screenshots
from .testimonial_engine import generate_testimonials, save_testimonials
from .review_engine import generate_review_stats, save_review_stats
from .benefit_engine import generate_benefits, generate_benefit_summary, save_benefits
from .value_score_engine import compute_value_score, save_value_score

def build_vault_preview(vault_path: str, metadata: dict):
    # 1. Outline
    outline = extract_outline_from_pdf_or_md(vault_path)
    save_outline(vault_path, outline)
    # 2. Screenshots
    screenshots = generate_pdf_screenshots(vault_path, num_pages=2)
    # 3. Testimonials
    testimonials = generate_testimonials(metadata.get('title', ''), metadata.get('niche', 'misc'))
    save_testimonials(vault_path, testimonials)
    # 4. Reviews
    review_stats = generate_review_stats(metadata.get('title', ''), vault_quality=metadata.get('content_quality_score', 1))
    save_review_stats(vault_path, review_stats)
    # 5. Benefits
    benefits = generate_benefits(metadata.get('title', ''), metadata.get('niche', 'misc'))
    benefit_summary = generate_benefit_summary(metadata.get('title', ''), metadata.get('niche', 'misc'))
    save_benefits(vault_path, benefits, benefit_summary)
    # 6. Value Score
    value_score = compute_value_score(metadata, outline)
    save_value_score(vault_path, value_score)
    # 7. Final vault_preview.json auto-compile (ensure all fields)
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    with open(preview_path, 'r') as f:
        preview = json.load(f)
    preview.update({
        'title': metadata.get('title', ''),
        'outline': outline,
        'screenshots': screenshots,
        'testimonials': testimonials,
        'avg_rating': review_stats.get('avg_rating', 4.8),
        'total_reviews': review_stats.get('total_reviews', 22),
        'benefits': benefits,
        'benefit_summary': benefit_summary,
        'value_score': value_score
    })
    with open(preview_path, 'w') as f:
        json.dump(preview, f, indent=2)
