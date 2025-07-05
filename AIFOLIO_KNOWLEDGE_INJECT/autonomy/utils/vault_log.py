def log_vault_event(vault_id, event, payload, errors):
    print(f"[VAULT LOG] {event} for vault {vault_id}: {payload} ERRORS: {errors}")


def log_activity(vault_id, event, payload, errors):
    print(f"[ACTIVITY LOG] {event} for vault {vault_id}: {payload} ERRORS: {errors}")
