# WIND_PLACEHOLDER
def apply_style_tuning(text, tone="bold", format="markdown"):
    if tone == "bold":
        return f"**{text}**"
    elif tone == "italic":
        return f"*{text}*"
    return text
