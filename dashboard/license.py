"""
license.py — License Management Blueprint
Elite security, ethics, and maintainability: CSRF, audit logging, modular.
"""
from flask import Blueprint, render_template, request
import json
import os
from datetime import datetime

LICENSE_CONFIG = os.path.join(os.path.dirname(__file__), '../config/license_mode.json')

license_bp = Blueprint('license', __name__, template_folder='templates')

# --- Security Utilities (assume import or define here as needed) ---
def validate_csrf_token(token):
    from dashboard.web_dashboard import validate_csrf_token as vct
    return vct(token)

def generate_csrf_token():
    from dashboard.web_dashboard import generate_csrf_token as gct
    return gct()

@license_bp.route('/license', methods=['GET', 'POST'])
def license_management():
    """License management with CSRF and double audit log."""
    with open(LICENSE_CONFIG, 'r') as f:
        config = json.load(f)
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not validate_csrf_token(token):
            return "CSRF validation failed", 400
        mode = request.form.get('mode')
        if mode:
            config['mode'] = mode
            with open(LICENSE_CONFIG, 'w') as f2:
                json.dump(config, f2, indent=2)
            for logf in ['../analytics/audit_trail.log', '../analytics/audit_trail_backup.log']:
                with open(logf, 'a') as f:
                    f.write(f"LICENSE_MODE_SET: {mode} by {request.remote_addr} at {datetime.now()}\n")
    modes = ['private', 'gift', 'paid', 'subscription', 'auto_mode']
    csrf_token = generate_csrf_token()
    form = '<form method="post">' + ''.join([f'<label><input type="radio" name="mode" value="{m}" {"checked" if config["mode"]==m else ""}/> {m.title()}</label><br>' for m in modes]) + f'<input type="hidden" name="csrf_token" value="{csrf_token}"/><button type="submit">Set Mode</button></form>'
    return render_template('dashboard.html', content=f"<h3>License Management</h3>{form}<a href='/dashboard'>Back</a>")

# --- TODO: Add further license management endpoints as needed for modularity, security, and ethics. ---
