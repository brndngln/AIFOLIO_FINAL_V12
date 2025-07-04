def detect_niche_from_title(title):
    title = title.lower()
    if any(keyword in title for keyword in ["client", "freelance", "contract"]):
        return "freelancer"
    elif any(keyword in title for keyword in ["coach", "program", "growth"]):
        return "coach"
    elif any(keyword in title for keyword in ["pride", "queer", "lgbtq", "trans", "nonbinary"]):
        return "lgbtq"
    else:
        return "general"