# All valid event types for the AIFOLIO event pipeline

# Payment / Transaction Events
EVENT_PAYMENT_FAILED = "payment_failed"
EVENT_PAYMENT_RETRIED = "payment_retried"
EVENT_SUBSCRIPTION_RENEWED = "subscription_renewed"
EVENT_CHARGEBACK_RECEIVED = "chargeback_received"

# Refund / Dispute Events
EVENT_REFUND_INITIATED = "refund_initiated"
EVENT_REFUND_APPROVED = "refund_approved"
EVENT_REFUND_DENIED = "refund_denied"

# Compliance / Legal Flows
EVENT_POLICY_REVOKED = "policy_revoked"
EVENT_GDPR_DATA_REQUEST = "gdpr_data_request"
EVENT_GDPR_DATA_DELETED = "gdpr_data_deleted"

# User Engagement Flows
EVENT_VAULT_VIEWED = "vault_viewed"
EVENT_UPSELL_VIEWED = "upsell_viewed"
EVENT_CART_ABANDONED = "cart_abandoned"
EVENT_WISHLIST_ADDED = "wishlist_added"

# Storefront / Catalog Flows
EVENT_VAULT_HIDDEN = "vault_hidden"
EVENT_VAULT_RELISTED = "vault_relisted"
EVENT_VAULT_VERSION_UPDATED = "vault_version_updated"

# System Health / Error Flows
EVENT_HOOK_FAILED = "hook_failed"
EVENT_AI_VALIDATION_FAILED = "ai_validation_failed"
EVENT_EXPORT_TIMEOUT = "export_timeout"
EVENT_DELIVERY_DELAYED = "delivery_delayed"

# Security / Account Flows
EVENT_LOGIN_SUCCESS = "login_success"
EVENT_LOGIN_FAILED = "login_failed"
EVENT_IP_BLOCKED = "ip_blocked"
EVENT_ADMIN_ACTION_TAKEN = "admin_action_taken"

# AI Enhancer Flows (SAFE)
EVENT_AI_AUDIT_PASSED = "ai_audit_passed"
EVENT_AI_AUDIT_FLAGGED = "ai_audit_flagged"
EVENT_AI_TONE_MATCH_PASSED = "ai_tone_match_passed"
EVENT_AI_ACCESSIBILITY_PASSED = "ai_accessibility_passed"

EVENT_VAULT_CREATED = "vault_created"
EVENT_VAULT_PUBLISHED = "vault_published"
EVENT_VAULT_SOLD = "vault_sold"
EVENT_VAULT_REFUNDED = "vault_refunded"
EVENT_DELIVERY_SENT = "delivery_sent"
EVENT_RECEIPT_CREATED = "receipt_created"
EVENT_VAULT_DOWNLOADED = "vault_downloaded"
EVENT_VAULT_METADATA_UPDATED = "vault_metadata_updated"
EVENT_UPSELL_TRIGGERED = "upsell_triggered"
EVENT_POLICY_SIGNED = "policy_signed"
EVENT_EXPORT_FAILED = "export_failed"
EVENT_VAULT_TEST_RUN = "vault_test_run"
EVENT_VAULT_FULFILLED = "vault_fulfilled"
EVENT_REFUND_ISSUED = "refund_issued"
EVENT_DOWNLOAD_INITIATED = "download_initiated"
EVENT_POLICY_VIOLATED = "policy_violated"
EVENT_VAULT_FLAGGED_FOR_REVIEW = "vault_flagged_for_review"
EVENT_VAULT_EXPIRED = "vault_expired"
EVENT_REFUND_INITIATED = "refund_initiated"
EVENT_VAULT_FAILED_BUILD = "vault_failed_build"

ALL_EVENTS = [
    # Payment / Transaction Events
    EVENT_PAYMENT_FAILED,
    EVENT_PAYMENT_RETRIED,
    EVENT_SUBSCRIPTION_RENEWED,
    EVENT_CHARGEBACK_RECEIVED,
    # Refund / Dispute Events
    EVENT_REFUND_INITIATED,
    EVENT_REFUND_APPROVED,
    EVENT_REFUND_DENIED,
    # Compliance / Legal Flows
    EVENT_POLICY_REVOKED,
    EVENT_GDPR_DATA_REQUEST,
    EVENT_GDPR_DATA_DELETED,
    # User Engagement Flows
    EVENT_VAULT_VIEWED,
    EVENT_UPSELL_VIEWED,
    EVENT_CART_ABANDONED,
    EVENT_WISHLIST_ADDED,
    # Storefront / Catalog Flows
    EVENT_VAULT_HIDDEN,
    EVENT_VAULT_RELISTED,
    EVENT_VAULT_VERSION_UPDATED,
    # System Health / Error Flows
    EVENT_HOOK_FAILED,
    EVENT_AI_VALIDATION_FAILED,
    EVENT_EXPORT_TIMEOUT,
    EVENT_DELIVERY_DELAYED,
    # Security / Account Flows
    EVENT_LOGIN_SUCCESS,
    EVENT_LOGIN_FAILED,
    EVENT_IP_BLOCKED,
    EVENT_ADMIN_ACTION_TAKEN,
    # AI Enhancer Flows (SAFE)
    EVENT_AI_AUDIT_PASSED,
    EVENT_AI_AUDIT_FLAGGED,
    EVENT_AI_TONE_MATCH_PASSED,
    EVENT_AI_ACCESSIBILITY_PASSED,
    # Existing Events
    EVENT_VAULT_CREATED,
    EVENT_VAULT_PUBLISHED,
    EVENT_VAULT_SOLD,
    EVENT_VAULT_REFUNDED,
    EVENT_DELIVERY_SENT,
    EVENT_RECEIPT_CREATED,
    EVENT_VAULT_DOWNLOADED,
    EVENT_VAULT_METADATA_UPDATED,
    EVENT_UPSELL_TRIGGERED,
    EVENT_POLICY_SIGNED,
    EVENT_EXPORT_FAILED,
    EVENT_VAULT_TEST_RUN,
    EVENT_VAULT_FULFILLED,
    EVENT_REFUND_ISSUED,
    EVENT_DOWNLOAD_INITIATED,
    EVENT_POLICY_VIOLATED,
    EVENT_VAULT_FLAGGED_FOR_REVIEW,
    EVENT_VAULT_EXPIRED,
    EVENT_VAULT_FAILED_BUILD,
]
