"""
SAFE AI static vault tag optimization suggester
- Suggests additional tags based on static keyword matching
- 100% static, non-sentient, suggest-only
"""


def suggest_tags(vault_content, tag_library):
    suggestions = [tag for tag in tag_library if tag in vault_content]
    return suggestions
