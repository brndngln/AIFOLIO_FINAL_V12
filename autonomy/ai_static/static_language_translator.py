"""
AIFOLIO™ SAFE AI MODULE: Static Language Translator
- Static only. No static, no loops or self-calling functions, or static logic.
- Translates legal policy markdowns using pre-approved translation tables.
- No generative translation. All mappings are human-reviewed.
"""
import os
import json
import logging

TRANSLATION_TABLE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../distribution/legal_exports/translation_table.json",
    )
)
LOG_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../distribution/legal_exports/translation_log.txt",
    )
)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


from typing import Dict

def static_translate(text: str, language: str) -> str:
    if not os.path.exists(TRANSLATION_TABLE_PATH):
        logging.error("Translation table missing.")
        return text
    with open(TRANSLATION_TABLE_PATH, "r") as f:
        table = json.load(f)
    mapping = table.get(language, {})
    for k, v in mapping.items():
        text = text.replace(k, v)
    logging.info(f"Static translation performed for {language}.")
    return text
