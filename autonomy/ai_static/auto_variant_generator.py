"""
AIFOLIO™ SAFE AI MODULE: Auto-Variant Generator
- Static, non-sentient
- Generates output variants from pre-approved templates
- All variants require human approval
- No autonomous content creation
"""


def generate_variants(text, templates):
    return [template.format(text=text) for template in templates]
