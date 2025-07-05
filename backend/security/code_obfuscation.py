"""
AIFOLIO Codebase Obfuscation Layer
Static, deterministic, SAFE AI-compliant code obfuscation config and audit logger.
"""
import logging

logger = logging.getLogger(__name__)

OBFUSCATION_METHODS = [
    "pyarmor (Python)",
    "js-obfuscator (JS)",
    "webpack --mode=production (JS)",
]

STATIC_OBFUSCATION_CONFIG = {
    "python": "pyarmor obfuscate --recursive ./aifolio_empire",
    "js": "npx javascript-obfuscator ./dashboard --output ./dashboard/dist",
    "webpack": "npx webpack --mode=production",
}


def get_obfuscation_methods() -> list:
    logger.info(f"Obfuscation methods: {OBFUSCATION_METHODS}")
    return OBFUSCATION_METHODS


def get_obfuscation_config(lang: str) -> str:
    config = STATIC_OBFUSCATION_CONFIG.get(lang, "")
    logger.info(f"Obfuscation config for {lang}: {config}")
    return config
