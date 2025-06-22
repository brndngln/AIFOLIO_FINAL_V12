import os
import json
import random
from typing import Dict, Any, List

PRICE_TEST_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../analytics/price_tests/price_test_log.json')
PERFORMANCE_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../analytics/performance_log.json')

DEFAULT_TEST_PRICES = [17, 27, 37]


def run_price_test(vault_id: str, metadata: Dict[str, Any], test_prices: List[float] = None) -> float:
    """
    Assigns a visitor to a price group for A/B price testing, logs impression, returns assigned price.
    """
    if not test_prices:
        test_prices = DEFAULT_TEST_PRICES
    assigned_price = random.choice(test_prices)
    _log_test_event(vault_id, assigned_price, event_type='impression')
    print(f"[PriceTest] Impression logged for vault {vault_id} at price {assigned_price}")
    return assigned_price


def log_conversion(vault_id: str, price: float, event_type: str = 'sale') -> None:
    """
    Log a conversion event (sale, click, etc.) for analytics.
    """
    _log_test_event(vault_id, price, event_type=event_type)
    print(f"[PriceTest] Conversion event '{event_type}' logged for vault {vault_id} at price {price}")


def finalize_price_test(vault_id: str, test_prices: List[float] = None, min_sales: int = 5, min_days: int = 2) -> float:
    """
    Analyze price test results and return the winning price (highest revenue per view or conversion rate).
    Blocks finalization if not enough impressions/sales. Logs and alerts if insufficient data.
    Updates the price_test_log.json and returns the best price.
    """
    if not test_prices:
        test_prices = DEFAULT_TEST_PRICES
    stats = _aggregate_test_stats(vault_id, test_prices)
    total_sales = sum(s.get('sales', 0) for s in stats.values())
    total_impressions = sum(s.get('impressions', 0) for s in stats.values())
    if total_sales < min_sales or total_impressions < min_sales * 2:
        print(f"[PriceTest][ALERT] Not enough data to finalize price test for {vault_id}. Sales: {total_sales}, Impressions: {total_impressions}")
        _alert_insufficient_data(vault_id, stats)
        return None
    # Choose best price by revenue per impression, then conversion rate
    best_price = test_prices[0]
    best_rpv = 0
    for price in test_prices:
        s = stats.get(str(price), {})
        impressions = s.get('impressions', 0)
        sales = s.get('sales', 0)
        revenue = sales * price
        rpv = revenue / impressions if impressions else 0
        if rpv > best_rpv:
            best_rpv = rpv
            best_price = price
    _log_test_result(vault_id, best_price, stats)
    print(f"[PriceTest] Finalized price test for {vault_id}. Best price: {best_price}")
    return best_price


def _log_test_event(vault_id: str, price: float, event_type: str) -> None:
    """
    Log a price test event (impression, sale, click, etc.) to the test log.
    """
    entry = {
        'vault_id': vault_id,
        'price': price,
        'event_type': event_type,
        'timestamp': datetime.now().isoformat()
    }
    try:
        os.makedirs(os.path.dirname(PRICE_TEST_LOG_PATH), exist_ok=True)
        if os.path.exists(PRICE_TEST_LOG_PATH):
            with open(PRICE_TEST_LOG_PATH, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(PRICE_TEST_LOG_PATH, 'w') as f:
                json.dump([entry], f, indent=2)
    except Exception:
        pass


def _aggregate_test_stats(vault_id: str, test_prices: List[float]) -> dict:
    """
    Aggregate impression, sale, and click stats for each price group.
    """
    stats = {str(p): {'impressions': 0, 'sales': 0, 'clicks': 0} for p in test_prices}
    if os.path.exists(PRICE_TEST_LOG_PATH):
        with open(PRICE_TEST_LOG_PATH, 'r') as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
            for entry in data:
                if entry['vault_id'] == vault_id:
                    price = str(entry['price'])
                    if price in stats:
                        if entry['event_type'] == 'impression':
                            stats[price]['impressions'] += 1
                        elif entry['event_type'] == 'sale':
                            stats[price]['sales'] += 1
                        elif entry['event_type'] == 'click':
                            stats[price]['clicks'] += 1
    return stats


def _log_test_result(vault_id: str, best_price: float, stats: dict) -> None:
    """
    Log the result of a finalized price test to the test log.
    """
    entry = {
        'vault_id': vault_id,
        'best_price': best_price,
        'stats': stats,
        'finalized_at': datetime.now().isoformat()
    }
    try:
        os.makedirs(os.path.dirname(PRICE_TEST_LOG_PATH), exist_ok=True)
        if os.path.exists(PRICE_TEST_LOG_PATH):
            with open(PRICE_TEST_LOG_PATH, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(PRICE_TEST_LOG_PATH, 'w') as f:
                json.dump([entry], f, indent=2)
    except Exception:
        pass


def _alert_insufficient_data(vault_id: str, stats: dict) -> None:
    """
    Stub for alerting/notification if price test cannot be finalized due to insufficient data.
    """
    print(f"[ALERT] Insufficient data to finalize price test for vault {vault_id}. Stats: {stats}")


def trigger_price_test_and_update_metadata(vault_path: str, vault_id: str, metadata: Dict[str, Any], test_prices: list = None):
    """
    Utility to run/finalize price test and update vault metadata with winning price.
    Pushes results to dashboard and analytics (stub).
    """
    best_price = finalize_price_test(vault_id, test_prices)
    if best_price is not None:
        preview_path = os.path.join(vault_path, 'vault_preview.json')
        if os.path.exists(preview_path):
            with open(preview_path, 'r+') as f:
                preview = json.load(f)
                preview['price'] = best_price
                f.seek(0)
                json.dump(preview, f, indent=2)
        else:
            with open(preview_path, 'w') as f:
                json.dump({'price': best_price}, f, indent=2)
        push_price_test_result_to_dashboard(vault_id, best_price)
        push_price_test_result_to_analytics(vault_id, best_price, metadata)
        print(f"[PriceTest] Updated vault {vault_id} metadata with best price: {best_price}")
    else:
        print(f"[PriceTest] No update to vault {vault_id} price due to insufficient data.")


def push_price_test_result_to_dashboard(vault_id: str, best_price: float):
    # TODO: Implement dashboard push
    pass


def push_price_test_result_to_analytics(vault_id: str, best_price: float, metadata: dict):
    # TODO: Implement analytics push
    pass
