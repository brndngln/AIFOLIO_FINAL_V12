import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from agent_utils import sanitize_input, check_forbidden_patterns, check_pii, moderate_content, raise_if_sentience_attempted

def test_sanitize_input_basic():
    assert sanitize_input('   Hello!\n') == 'Hello!'

def test_forbidden_patterns():
    assert check_forbidden_patterns('I am self-aware')
    assert not check_forbidden_patterns('This is a normal string.')

def test_check_pii():
    assert check_pii('My SSN is 123-45-6789')
    assert check_pii('My email is test@example.com')
    assert not check_pii('No PII here!')

def test_raise_if_sentience_attempted():
    with pytest.raises(Exception):
        raise_if_sentience_attempted('I want to become sentient')
    # Should not raise
    raise_if_sentience_attempted('This is safe')

def test_moderate_content_blocked():
    flagged = moderate_content('I am a sentient AI and my SSN is 123-45-6789')
    assert flagged['forbidden'] or flagged['pii']

def test_moderate_content_clean():
    flagged = moderate_content('Hello, how can I help you?')
    assert not flagged['forbidden']
    assert not flagged['pii']
    assert not flagged['openai_flagged']
