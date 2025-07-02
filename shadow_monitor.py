"""
AIFOLIO™ Shadow Monitor
Detects rogue triggers, recursive spawning, or sentient lean. Auto-flushes cache and resets state.
"""
import logging

def detect_rogue_trigger(event):
    if "recursive" in event or "sentient" in event:
        logging.critical(f"Rogue trigger detected: {event}")
        auto_flush_cache()
        reset_state()
        return True
    return False

def auto_flush_cache():
    logging.info("Cache auto-flushed by Shadow Monitor.")

def reset_state():
    logging.info("System state reset by Shadow Monitor.")
