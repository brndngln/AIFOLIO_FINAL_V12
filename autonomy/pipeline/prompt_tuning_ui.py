import streamlit as st
import hashlib
import json
import os
import datetime
from spellchecker import SpellChecker

PROMPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompts'))
AUDIT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/prompt_audit_log.jsonl'))
os.makedirs(PROMPT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

ANTI_PATTERNS = [
    'as an ai', 'ignore previous', 'regenerate', 'write a story', 'be creative',
    'pretend you are', 'you are sentient', 'act as', 'simulate', 'imagine you are'
]

# --- Helper Functions ---
def fingerprint_prompt(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def spell_check(text, lang='en'):
    spell = SpellChecker(language=lang)
    errors = list(spell.unknown(text.split()))
    return errors

def detect_anti_patterns(text):
    found = [p for p in ANTI_PATTERNS if p in text.lower()]
    return found

def log_audit(action, before, after, user='admin'):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'action': action,
        'user': user,
        'before': before,
        'after': after,
        'before_fingerprint': fingerprint_prompt(before or ''),
        'after_fingerprint': fingerprint_prompt(after or '')
    }
    with open(AUDIT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def load_prompts():
    prompts = {}
    for fname in os.listdir(PROMPT_DIR):
        if fname.endswith('.txt'):
            with open(os.path.join(PROMPT_DIR, fname), 'r') as f:
                prompts[fname[:-4]] = f.read()
    return prompts

def save_prompt(name, text):
    with open(os.path.join(PROMPT_DIR, f'{name}.txt'), 'w') as f:
        f.write(text)

# --- Streamlit UI ---
st.title('AIFOLIO™ Prompt Tuning UI (Non-Sentient Safe)')
prompts = load_prompts()
selected = st.selectbox('Select prompt to edit', list(prompts.keys()) + ['<Create New>'])
if selected == '<Create New>':
    prompt_name = st.text_input('Prompt Name')
    prompt_text = ''
else:
    prompt_name = selected
    prompt_text = prompts[selected]

edited_prompt = st.text_area('Prompt Text', prompt_text, height=200)

if st.button('Preview AI Output'):
    # Example deterministic preview (stub)
    st.info(f"[PREVIEW] This is what the AI would output for: {edited_prompt[:60]}...")

anti_patterns = detect_anti_patterns(edited_prompt)
spell_errors = spell_check(edited_prompt)
fingerprint = fingerprint_prompt(edited_prompt)

st.write(f'**Prompt Fingerprint:** `{fingerprint}`')
if anti_patterns:
    st.warning(f"Anti-patterns detected: {', '.join(anti_patterns)}")
if spell_errors:
    st.warning(f"Spelling errors detected: {', '.join(spell_errors)}")

if st.button('Save Prompt (Requires Human Approval)'):
    if not prompt_name:
        st.error('Prompt name required.')
    elif anti_patterns:
        st.error('Cannot save: Anti-patterns detected.')
    else:
        before = prompts.get(prompt_name, '')
        save_prompt(prompt_name, edited_prompt)
        log_audit('edit', before, edited_prompt)
        st.success('Prompt saved and logged. Awaiting human approval.')
        st.write(f'Fingerprint: {fingerprint}')
        st.write('Audit log entry created.')

# Human approval queue (for admins)
if st.checkbox('Show audit log (admin only)'):
    if os.path.exists(AUDIT_LOG):
        with open(AUDIT_LOG, 'r') as f:
            for line in f.readlines()[-20:]:
                st.code(line.strip())
    else:
        st.info('No audit log entries yet.')
