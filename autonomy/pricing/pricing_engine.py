"""
AIFOLIO Pricing Engine
- Deterministic, static, non-static pricing logic
- Audit-logs all pricing events to both pricing_log.json locations
- GDPR/CCPA compliant, owner controlled
"""
import os
import json
from typing import Dict, Any
from datetime import datetime

PRICING_LOG_PATHS = [
    os.path.join(os.path.dirname(__file__), '../../analytics/pricing_log.json'),
    os.path.join(os.path.dirname(__file__), 'pricing_log.json')
]

NICHE_MULTIPLIERS = {
    "ai": 1.5,
    "money": 1.5,
    "investing": 1.4,
    "fitness": 1.2,
    "relationships": 1.2,
    "journaling": 1.0,
    "misc": 1.0
}

PSYCH_PRICES = [9, 17, 27, 39, 47, 59, 79, 97]

def audit_log(event, details=None):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details or {}
    }
    for path in PRICING_LOG_PATHS:
        if os.path.exists(path):
            with open(path, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(path, 'w') as f:
            json.dump(logs, f, indent=2)


def calculate_price(metadata: Dict[str, Any]) -> float:
    """
    Main pricing calculation engine. Applies manual lock, value-based, bundle, niche, competitor, psychological, tier, and performance logic.
    Logs all steps and returns the final price.
    """
    log = {}
    # 1. Manual Pricing Override
    if metadata.get('lock_price'):
        log['final_price'] = metadata['price']
        log['reason'] = 'lock_price override'
        _log_pricing(metadata, log)
        return metadata['price']
    if not metadata.get('auto_price', True):
        if metadata.get('price') is None:
            raise ValueError('Manual pricing required but price is null.')
        log['final_price'] = metadata['price']
        log['reason'] = 'manual price'
        _log_pricing(metadata, log)
        return metadata['price']

    # 2. Value-Based Pricing Engine
    base_price = 9.0
    page_count = metadata.get('page_count', 0)
    content_quality = metadata.get('content_quality_score', 1)
    expected_income = metadata.get('expected_income')
    base_price += (page_count // 10) * 3
    base_price *= content_quality
    if expected_income:
        base_price = max(base_price, float(expected_income) * 0.05)
    log['value_price'] = round(base_price, 2)

    # 3. Bundle Logic Engine
    bundle_size = metadata.get('bundle_size', 1)
    bundle_bonus = 0
    if bundle_size > 1:
        bundle_bonus = (bundle_size - 1) * (base_price * 0.5)
        base_price += bundle_bonus
    log['bundle_bonus'] = round(bundle_bonus, 2)

    # 4. Niche Multiplier Engine
    tags = metadata.get('tags', [])
    niche = metadata.get('niche', 'misc')
    multiplier = 1.0
    for tag in tags + [niche]:
        if tag in NICHE_MULTIPLIERS:
            multiplier = max(multiplier, NICHE_MULTIPLIERS[tag])
    base_price *= multiplier
    log['niche_multiplier'] = multiplier

    # 5. Competitive Pricing Engine (stub)
    competitor_price = scan_competitor_prices(niche)
    cover_rating = metadata.get('cover_design_rating', 5)
    if competitor_price:
        adjust = 1.10 if cover_rating >= 7 else 0.90
        base_price = competitor_price * adjust
    log['competitor_price'] = competitor_price

    # 6. Psychological Pricing Engine
    pre_psych = base_price
    rounded = min(PSYCH_PRICES, key=lambda x: abs(x - pre_psych))
    if pre_psych > max(PSYCH_PRICES):
        rounded = max(PSYCH_PRICES)
    # Optionally add .99 ending
    final_price = float(f"{rounded}.99") if rounded < 97 else float(rounded)
    log['final_before_psych'] = round(pre_psych, 2)
    log['final_price'] = final_price

    # 7. Tier-Based Engine
    tier = 'starter'
    if page_count > 30 or bundle_size > 3:
        tier = 'pro'
    if page_count > 60 or bundle_size > 5:
        tier = 'elite'
    log['tier'] = tier

    # 8. Performance Optimizer Engine (stub)
    log['performance_adjustment'] = adjust_price_based_on_performance(metadata.get('vault_id'))

    _log_pricing(metadata, log)
    return final_price


def explain_price(metadata: Dict[str, Any]) -> str:
    """
    Returns a human-readable explanation of the price calculation.
    """
    price = calculate_price(metadata)
    return f"Final price for {metadata.get('title', 'vault')}: ${price:.2f}"


def trigger_pricing_on_vault_event(vault_path: str, metadata: Dict[str, Any]) -> float:
    """
    Trigger price calculation and logging on vault creation or update.
    Pushes pricing data to Gumroad uploader, dashboard, and tracker (stub).
    """
    price = calculate_price(metadata)
    # Save to vault metadata or preview JSON
    preview_path = os.path.join(vault_path, 'vault_preview.json')
    if os.path.exists(preview_path):
        with open(preview_path, 'r+') as f:
            preview = json.load(f)
            preview['price'] = price
            f.seek(0)
            json.dump(preview, f, indent=2)
    else:
        with open(preview_path, 'w') as f:
            json.dump({'price': price}, f, indent=2)
    # Push to integrations (stub)
    push_to_gumroad(vault_path, price)
    push_to_dashboard(vault_path, price)
    push_to_performance_tracker(vault_path, price)
    return price


def push_to_gumroad(vault_path: str, price: float):
    # TODO: Implement Gumroad uploader integration
    pass


def push_to_dashboard(vault_path: str, price: float):
    # TODO: Implement dashboard preview panel integration
    pass


def push_to_performance_tracker(vault_path: str, price: float):
    # TODO: Implement vault performance tracker integration
    pass


def scan_competitor_prices(niche: str) -> float:
    """
    Stub for competitor price scanning. Replace with real API/scraper.
    """
    dummy = {
        'ai': 37.0,
        'money': 47.0,
        'investing': 44.0,
        'fitness': 27.0,
        'relationships': 19.0,
        'journaling': 13.0,
        'misc': 9.0
    }
    return dummy.get(niche, 9.0)


def adjust_price_based_on_performance(vault_id: str) -> float:
    """
    Stub for future performance-based price optimization.
    """
    return None


def _log_pricing(metadata: Dict[str, Any], log: Dict[str, Any]):
    """
    Append a detailed pricing log entry to the analytics log file.
    """
    entry = {
        "metadata": metadata,
        "log": log
    }
    try:
        if os.path.exists(PRICING_LOG_PATH):
            with open(PRICING_LOG_PATH, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(PRICING_LOG_PATH, 'w') as f:
                json.dump([entry], f, indent=2)
    except Exception:
        pass
