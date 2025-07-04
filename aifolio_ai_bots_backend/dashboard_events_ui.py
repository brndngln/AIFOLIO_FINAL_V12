"""
AIFOLIO™ Dashboard Integration + UI
Events tab, real-time feed, manual triggers, schema editor, overlays, and lockdown on sentience signal.
"""
import logging

DASHBOARD_EVENTS = []
DASHBOARD_LOCKED = False


def add_event(event):
    DASHBOARD_EVENTS.append(event)
    logging.info(f"Dashboard event: {event}")
    return True

def get_event_feed():
    return DASHBOARD_EVENTS[-50:]

def manual_retrigger(event_id):
    logging.info(f"Manual re-trigger of event {event_id}")
    return True

def lock_dashboard_if_sentience(signal_detected):
    global DASHBOARD_LOCKED
    if signal_detected:
        DASHBOARD_LOCKED = True
        logging.critical("Dashboard locked due to sentience signal!")
    return DASHBOARD_LOCKED
