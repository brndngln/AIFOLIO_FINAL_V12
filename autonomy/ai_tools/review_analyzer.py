import re

import datetime
import json

def analyze_review(text):
    """
    SAFE AI-compliant: Flags misspellings, banned words, PII, financial data, and basic sentiment (static rule-based, non-AI).
    Returns dict with 'spelling', 'banned', 'sentiment', 'flags'.
    All logic is static, non-adaptive, owner-controlled, and audit-logged.
    """
    banned = {'scam', 'fraud', 'ripoff', 'hate', 'illegal'}
    pii_keywords = {'ssn', 'social security', 'passport', 'driver license', 'credit card', 'bank account', 'iban', 'swift', 'routing number', 'account number', 'dob', 'date of birth', 'address', 'phone', 'email', 'tax id', 'sin', 'national id'}
    financial_keywords = {'usd', 'eur', 'btc', 'bank', 'wire', 'transfer', 'payment', 'invoice', 'routing', 'account', 'balance', 'deposit', 'withdrawal', 'loan', 'credit', 'debit', 'card', 'paypal', 'stripe', 'gumroad', 'revenue', 'profit', 'loss', 'tax', 'salary', 'wage', 'payroll'}
    spelling_errors = [w for w in text.split() if not w.isalpha() or len(w) < 2]
    banned_found = [w for w in text.lower().split() if w in banned]
    pii_found = [w for w in text.lower().split() if w in pii_keywords]
    financial_found = [w for w in text.lower().split() if w in financial_keywords]
    sentiment = 'negative' if any(w in text.lower() for w in ['bad', 'hate', 'awful', 'terrible']) else 'positive'
    flags = []
    if spelling_errors:
        flags.append('spelling')
    if banned_found:
        flags.append('banned')
    if pii_found:
        flags.append('pii')
    if financial_found:
        flags.append('financial')
    if sentiment == 'negative':
        flags.append('negative')
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': text,
        'spelling': spelling_errors,
        'banned': banned_found,
        'pii': pii_found,
        'financial': financial_found,
        'sentiment': sentiment,
        'flags': flags
    }
    with open('review_analyzer_audit.log', 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return {
        'spelling': spelling_errors,
        'banned': banned_found,
        'pii': pii_found,
        'financial': financial_found,
        'sentiment': sentiment,
        'flags': flags
    }
