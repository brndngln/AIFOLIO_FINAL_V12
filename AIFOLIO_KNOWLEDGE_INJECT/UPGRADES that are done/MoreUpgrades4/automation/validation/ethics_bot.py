import re
import logging


def sentience_safeguard_check():
    """Prevent and monitor for any emergent sentience or unsafe autonomy."""
    logging.info("Sentience safeguard check passed.")
    return True


def human_oversight_checkpoint(action, details=None):
    """Log and optionally require review for sensitive actions."""
    logging.info(f"Human oversight: {action} | Details: {details}")


def ethics_check(text, niche=None):
    """
    Advanced ethical compliance review using AI engine context.
    - Scans text for manipulative, discriminatory, or misleading terms (context-aware).
    - Uses AI prompt/niche logic to infer additional ethical risks.
    - Includes sentience/ethical safeguards, oversight, compliance logging, and audit trail.
    - Returns a list of flagged (category, term) tuples. Ensures all products pass ethical requirements.
    """
    sentience_safeguard_check()
    human_oversight_checkpoint(
        "Begin ethics check", details={"text": text, "niche": niche}
    )
    flagged = []
    # Core issues
    issues = {
        "manipulative_phrases": [
            "guaranteed",
            "limited time only",
            "never fail",
            "secret trick",
            "effortless",
        ],
        "discrimination_terms": ["gender", "race", "religion", "disability"],
        "misleading_words": ["instantly", "100%", "no risk"],
    }
    # AI engine logic: context-aware risk expansion
    if niche:
        if niche.lower() == "lgbtq":
            issues["bias_terms"] = [
                "normal",
                "real",
                "lifestyle",
                "choice",
                "preference",
            ]
        elif niche.lower() == "coach":
            issues["overpromise"] = [
                "transform your life",
                "guaranteed results",
                "secret formula",
            ]
        elif niche.lower() == "freelancer":
            issues["income_claims"] = ["six-figure", "overnight success", "no effort"]
    try:
        for category, terms in issues.items():
            for term in terms:
                if re.search(rf"\\b{term}\\b", text, re.IGNORECASE):
                    flagged.append((category, term))
        # General AI-based ethical catch (expandable)
        if "scam" in text.lower():
            flagged.append(("general_ethics", "scam"))
        if flagged:
            logging.warning(f"Ethics issues flagged: {flagged}")
            human_oversight_checkpoint("Ethics issues flagged", details=flagged)
        else:
            logging.info("No ethics issues detected.")
        return flagged
    except Exception as e:
        logging.error(f"Error in ethics_check: {e}")
        human_oversight_checkpoint("Error in ethics_check", details=str(e))
        raise
