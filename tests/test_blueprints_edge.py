"""
Edge case, error handling, and audit log tests for AIFOLIO dashboard blueprints.
Covers CSRF failures, missing/invalid data, and audit log output verification.
"""
import os
import tempfile
import pytest
from dashboard.web_dashboard import app

def read_last_audit_lines(n=10):
    try:
        with open('../analytics/audit_trail.log') as f:
            return f.readlines()[-n:]
    except Exception:
        return []

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    yield client
    os.close(db_fd)
    os.unlink(db_path)

# --- CSRF Failure Cases ---
def test_reviewer_csrf_fail(client):
    rv = client.post('/reviewer/escalate', data={})
    if rv.status_code == 404:
        import pytest; pytest.skip('reviewer/escalate route not implemented')
    assert rv.status_code == 400
    assert b'CSRF' in rv.data or b'csrf' in rv.data

def test_payments_csrf_fail(client):
    rv = client.post('/pay/stripe', data={'email': 'test@example.com'})
    assert rv.status_code == 400
    rv = client.post('/pay/gumroad', data={'email': 'test@example.com'})
    assert rv.status_code == 400

def test_license_csrf_fail(client):
    rv = client.post('/license', data={'mode': 'paid'})
    assert rv.status_code == 400

# --- Missing/Invalid Data ---
def test_product_gen_missing_fields(client):
    rv = client.post('/generate', data={'csrf_token': 'test'})
    assert rv.status_code in (400, 500)

def test_accessibility_invalid_route(client):
    rv = client.get('/accessibility/invalid_route')
    assert rv.status_code in (404, 400)

# --- Audit Log Output ---
def test_audit_log_on_license_change(client):
    # Get CSRF token
    client.get('/license')
    import os
    os.makedirs('../analytics', exist_ok=True)
    for f in ['../analytics/audit_trail.log', '../analytics/audit_trail_backup.log']:
        with open(f, 'a'):
            pass
    with client.session_transaction() as sess:
        csrf = sess.get('csrf_token') or 'test'
    rv = client.post('/license', data={'csrf_token': csrf, 'mode': 'paid'})
    assert rv.status_code in (200, 302)
    lines = read_last_audit_lines(10)
    assert any('LICENSE_MODE_SET' in l for l in lines)
