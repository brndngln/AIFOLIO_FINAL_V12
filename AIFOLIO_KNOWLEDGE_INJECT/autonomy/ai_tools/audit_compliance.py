def check_vault_metadata(metadata):
    """
    Checks for required fields and basic validity in vault metadata.
    Returns dict with 'missing', 'invalid', 'compliant' (True/False).
    Strictly static, non-AI.
    """
    required = [
        "vault_id",
        "title",
        "description",
        "creator_email",
        "created_at",
        "niche",
    ]
    missing = [f for f in required if not metadata.get(f)]
    invalid = []
    if "creator_email" in metadata and "@" not in metadata["creator_email"]:
        invalid.append("creator_email")
    compliant = not missing and not invalid
    return {"missing": missing, "invalid": invalid, "compliant": compliant}
