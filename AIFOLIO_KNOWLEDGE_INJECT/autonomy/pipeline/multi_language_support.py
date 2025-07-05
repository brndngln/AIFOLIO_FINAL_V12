import os
import json
import datetime
from spellchecker import SpellChecker

LANG_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/multi_language_log.jsonl")
)
os.makedirs(os.path.dirname(LANG_LOG), exist_ok=True)

FALSE_FRIENDS = {
    "es": {"actual": "current", "embarazada": "pregnant"},
    "fr": {"actuellement": "currently", "library": "bibliothèque"},
}


# --- Multi-language Generation ---
def check_language(text, lang="en"):
    spell = SpellChecker(language=lang)
    spelling_errors = list(spell.unknown(text.split()))
    # False friend detection
    false_friends = []
    if lang in FALSE_FRIENDS:
        for word, correct in FALSE_FRIENDS[lang].items():
            if word in text:
                false_friends.append(word)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "text": text,
        "lang": lang,
        "spelling_errors": spelling_errors,
        "false_friends": false_friends,
    }
    with open(LANG_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


if __name__ == "__main__":
    print(check_language("Este es un actual problema.", lang="es"))
