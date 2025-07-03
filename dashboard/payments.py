"""
payments.py — Payment (Stripe/Gumroad) Blueprint
Elite security, ethics, and maintainability: CSRF, audit logging, modular, privacy.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import json
from dashboard.payment_utils import process_stripe_payment, process_gumroad_payment

# --- Blueprint Setup ---
payments_bp = Blueprint('payments', __name__, template_folder='templates')

AUDIT_LOG = '../analytics/audit_trail.log'
AUDIT_BACKUP = '../analytics/audit_trail_backup.log'

# --- Security Utilities (assume import or define here as needed) ---
def validate_csrf_token(token):
    from dashboard.web_dashboard import validate_csrf_token as vct
    return vct(token)

def generate_csrf_token():
    from dashboard.web_dashboard import generate_csrf_token as gct
    return gct()

# --- Stripe Payment Endpoint ---
@payments_bp.route('/pay/stripe', methods=['POST'])
def pay_stripe():
    """Stripe payment endpoint with CSRF and double audit log."""
    token = request.form.get('csrf_token')
    if not validate_csrf_token(token):
        return jsonify({'status': 'CSRF validation failed'}), 400
    data = request.form
    result = process_stripe_payment(data)
    for logf in [AUDIT_LOG, AUDIT_BACKUP]:
        with open(logf, 'a') as f:
            f.write(f"PAYMENT_STRIPE: {data.get('email','')} {result} at {datetime.now()}\n")
    return jsonify({'status': result})

# --- Gumroad Payment Endpoint ---
@payments_bp.route('/pay/gumroad', methods=['POST'])
def pay_gumroad():
    """Gumroad payment endpoint with CSRF and double audit log."""
    token = request.form.get('csrf_token')
    if not validate_csrf_token(token):
        return jsonify({'status': 'CSRF validation failed'}), 400
    data = request.form
    result = process_gumroad_payment(data)
    for logf in [AUDIT_LOG, AUDIT_BACKUP]:
        with open(logf, 'a') as f:
            f.write(f"PAYMENT_GUMROAD: {data.get('email','')} {result} at {datetime.now()}\n")
    return jsonify({'status': result})

# --- TODO: Add further payment-related endpoints as needed for modularity, security, and ethics. ---
