import os
from googletrans import Translator

POLICY_PATHS = {
    "terms_of_service": "terms_of_service.md",
    "refund_policy": "refund_policy.md",
    "privacy_policy": "privacy_policy.md",
}


def translate_policy(policy_name: str, target_language: str = "en") -> str:
    """
    Translate the policy markdown to the requested language (static, on-demand).
    """
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, POLICY_PATHS.get(policy_name, ""))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Policy file {path} not found.")
    with open(path, "r") as f:
        text = f.read()
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text
