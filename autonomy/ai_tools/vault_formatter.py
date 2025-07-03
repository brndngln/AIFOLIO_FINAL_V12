import re

def format_title(title):
    """
    Capitalizes first letter of each word, strips extra whitespace, and fixes common grammar issues.
    Strictly rule-based, non-AI.
    """
    title = re.sub(r'\s+', ' ', title.strip())
    # Capitalize each word, but keep 'and', 'of', etc. lowercase unless first/last
    words = title.split()
    if not words:
        return ''
    small = {'and', 'of', 'the', 'in', 'on', 'at', 'for', 'with', 'to', 'a', 'an'}
    result = []
    for i, w in enumerate(words):
        if i == 0 or i == len(words)-1 or w.lower() not in small:
            result.append(w.capitalize())
        else:
            result.append(w.lower())
    return ' '.join(result)

def format_description(desc):
    """
    Cleans up whitespace, ensures first letter is capitalized, ends with period.
    Strictly rule-based, non-AI.
    """
    desc = re.sub(r'\s+', ' ', desc.strip())
    if not desc:
        return ''
    desc = desc[0].upper() + desc[1:]
    if not desc.endswith('.'):
        desc += '.'
    return desc
