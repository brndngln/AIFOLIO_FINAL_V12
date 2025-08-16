pt = None  # TODO: Define pt


def generate_prompt(topic, tags=None):
    base = f"Create a comprehensive guide on: {topic}"
    if tags:
        tag_line = "Include topics: " + ", ".join(tags)
        return f"{base}\n{tag_line}"
    return base
