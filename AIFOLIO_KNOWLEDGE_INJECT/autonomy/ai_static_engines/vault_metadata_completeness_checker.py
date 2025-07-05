"""
SAFE AI static vault metadata completeness checker
- Flags missing fields/tags in vaults (static rules only)
- 100% static, non-sentient, suggest-only
"""


def check_metadata_completeness(vault_metadata):
    required_fields = [
        "title",
        "description",
        "tags",
        "category",
        "owner",
        "created_at",
    ]
    missing = [field for field in required_fields if not vault_metadata.get(field)]
    return missing
