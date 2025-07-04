def legal_review(text, category="general"):
    required_disclaimers = {
        "finance": "This content is for informational purposes only and does not constitute financial advice.",
        "health": "Consult a licensed medical professional before following any advice in this guide.",
        "ai": "This product uses AI-generated content. Verify all critical information independently.",
        "business": "Earnings are not guaranteed. Your success depends on many personal factors."
    }

    warnings = []

    if category in required_disclaimers:
        disclaimer = required_disclaimers[category]
        if disclaimer not in text:
            warnings.append(f"Missing disclaimer for {category} content.")

    return warnings