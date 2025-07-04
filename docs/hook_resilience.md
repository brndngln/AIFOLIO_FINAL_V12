# Post-Sale Hook System Resilience

AIFOLIO™ post-sale hooks are engineered for maximum reliability, auditability, and safety, with strict non-sentient logic.

## Features

- **Retry Logic with Multi-Tiered Backoff:**
  - Short: 1m → 5m → 15m
  - Medium: 1h → 2h → 4h
  - Long: 1d → 2d
- **Centralized Error Handler:**
  - All retries/errors logged to `/logs/failed_hooks.log`
- **Manual Replay Command:**
  - CLI to replay failed hooks (one/all/filter)
- **Unit Test Stubs:**
  - Minimal test stubs for all hooks in `/tests/post_sale_hook_tests.py`
- **Hook Outcome Predictor:**
  - Predicts risk of hook delivery failure, warns and triggers fallback
- **Delivery Health Monitor:**
  - Monitors Postmark, Gumroad, and queue/webhook health
- **Refund Trigger Predictor:**
  - Detects refund risk patterns and flags for review
- **Hook Replay History Viewer:**
  - CLI/UI to view failed hooks and retry history
- **Hook Signature Fingerprinter:**
  - Adds signature hash to each hook payload for proof and traceability

## Usage

- Decorate hooks with `@retry_safe_hook(max_attempts=3, backoff_tier='short')`
- View `/logs/failed_hooks.log` for all retries and failures
- Use CLI command to replay failed hooks
- All logic is deterministic, business-aligned, and non-sentient

---

*See `retry_utils.py` and related modules for implementation details.*
