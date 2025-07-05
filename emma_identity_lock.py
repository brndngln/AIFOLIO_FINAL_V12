"""
EMMA Identity Lock: Hardcoded root identity verification and denial engine for all other users.
"""


def verify_owner(biometric_hash: str) -> bool:
    # Replace 'REPLACE_WITH_OWNER_HASH' with the actual owner's biometric hash
    OWNER_HASH = "REPLACE_WITH_OWNER_HASH"
    return biometric_hash == OWNER_HASH


def deny_non_owner(user_id: str):
    raise PermissionError(
        f"Access denied for user: {user_id}. Only the biometric-verified owner may access flirty/personality features."
    )
