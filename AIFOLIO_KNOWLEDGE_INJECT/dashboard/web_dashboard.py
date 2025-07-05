"""
AIFOLIO™ Owner Web Dashboard
- Owner-locked, no public access
- Modular tabs: Analytics, Compliance, Monetization, License Management
- Integrates all AI engines and PDF/product pipeline
"""
import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from dashboard.reviewer import reviewer_bp
from dashboard.accessibility import accessibility_bp
from dotenv import load_dotenv
from ai_engines.ethics_qualityguard import scan_and_fix

load_dotenv()

ADMIN_KEY = os.getenv("AIFOLIO_ADMIN_KEY")
LICENSE_CONFIG = os.path.join(os.path.dirname(__file__), "../config/license_mode.json")

app = Flask(__name__)
app.secret_key = os.environ.get("AIFOLIO_ADMIN_KEY", "insecure")
app.register_blueprint(reviewer_bp)
app.register_blueprint(accessibility_bp)

app.permanent_session_lifetime = 1800  # 30 minutes
# Elite session security
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# --- Brute-force lockout tracking ---
LOGIN_ATTEMPTS = {}
LOGIN_LOCKOUT = {}
LOCKOUT_THRESHOLD = 5
LOCKOUT_TIME = 900  # seconds (15 min)

# --- AI Oversight and Anti-Sentience Utility ---
from datetime import datetime


def anti_sentience_scan(obj):
    """Scan object for forbidden sentience attributes or behaviors."""
    forbidden = ["awareness", "self_modify", "persistent_memory", "recursive_self"]
    for attr in forbidden:
        if hasattr(obj, attr):
            raise RuntimeError(f"Sentience safeguard triggered: {attr} not allowed.")
    return True


def ai_action_with_oversight(input_data, engine_fn, context=""):
    """Run AI engine with full ethics, audit, and anti-sentience oversight."""
    scan_and_fix(input_data)
    result = engine_fn(input_data)
    scan_and_fix(result)
    anti_sentience_scan(engine_fn)
    # Audit log
    with open("../analytics/ai_audit.log", "a") as logf:
        logf.write(
            f"AI_ACTION|{datetime.now()}|{engine_fn.__name__}|Context:{context}|Input:{input_data}|Output:{result}\n"
        )
    # Double-backup
    with open("../analytics/ai_audit_backup.log", "a") as logf:
        logf.write(
            f"AI_ACTION|{datetime.now()}|{engine_fn.__name__}|Context:{context}|Input:{input_data}|Output:{result}\n"
        )
    return result


# --- CSRF Token Utility (simple) ---
def generate_csrf_token():
    import secrets

    token = secrets.token_hex(16)
    session["csrf_token"] = token
    return token


def validate_csrf_token(token):
    return token and session.get("csrf_token") == token


# --- Templates (for demo, use Jinja2 templates in production) ---
LOGIN_PAGE = """<form method="post"><input name="key" type="password" placeholder="Admin Key"/><button type="submit">Login</button></form>"""
DASHBOARD_PAGE = """<h2>AIFOLIO™ Owner Dashboard</h2>
<ul>
<li><a href="/analytics">Analytics</a></li>
<li><a href="/compliance">Compliance</a></li>
<li><a href="/monetization">Monetization</a></li>
<li><a href="/license">License Management</a></li>
<li><a href="/generate">Generate Product</a></li>
<li><a href="/logout">Logout</a></li>
</ul>"""


# --- Access Control ---
def owner_required(f):
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            flash("Login required.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@app.route("/", methods=["GET", "POST"])
def login():
    """Admin login with brute-force lockout and CSRF protection."""
    from time import time

    ip = request.remote_addr
    if ip in LOGIN_LOCKOUT and time() < LOGIN_LOCKOUT[ip]:
        msg = f"Locked out for {int((LOGIN_LOCKOUT[ip]-time())/60)} min."
        with open("../analytics/audit_trail.log", "a") as logf:
            logf.write(f"LOGIN_LOCKOUT: {ip} at {datetime.now()}\n")
        with open("../analytics/audit_trail_backup.log", "a") as logf:
            logf.write(f"LOGIN_LOCKOUT: {ip} at {datetime.now()}\n")
        return LOGIN_PAGE + f"<p>{msg}</p>"
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            return LOGIN_PAGE + "<p>CSRF validation failed</p>"
        if request.form["key"] == ADMIN_KEY:
            session["admin"] = True
            LOGIN_ATTEMPTS.pop(ip, None)
            LOGIN_LOCKOUT.pop(ip, None)
            with open("../analytics/audit_trail.log", "a") as logf:
                logf.write(f"LOGIN_SUCCESS: {ip} at {datetime.now()}\n")
            with open("../analytics/audit_trail_backup.log", "a") as logf:
                logf.write(f"LOGIN_SUCCESS: {ip} at {datetime.now()}\n")
            return redirect(url_for("dashboard"))
        LOGIN_ATTEMPTS[ip] = LOGIN_ATTEMPTS.get(ip, 0) + 1
        with open("../analytics/audit_trail.log", "a") as logf:
            logf.write(f"LOGIN_FAIL: {ip} at {datetime.now()}\n")
        with open("../analytics/audit_trail_backup.log", "a") as logf:
            logf.write(f"LOGIN_FAIL: {ip} at {datetime.now()}\n")
        if LOGIN_ATTEMPTS[ip] >= LOCKOUT_THRESHOLD:
            LOGIN_LOCKOUT[ip] = time() + LOCKOUT_TIME
            return (
                LOGIN_PAGE
                + "<p>Too many failed attempts. Locked out for 15 minutes.</p>"
            )
        return LOGIN_PAGE + "<p>Access Denied</p>"
    # GET: render login with CSRF
    csrf_token = generate_csrf_token()
    return LOGIN_PAGE.replace(
        "</form>",
        f'<input type="hidden" name="csrf_token" value="{csrf_token}"/></form>',
    )


@app.route("/dashboard")
@owner_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
@owner_required
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# --- Analytics & Compliance Tab Modularized ---
# TODO: Analytics and compliance endpoints are now in analytics.py (analytics_bp Blueprint)
# Import and register analytics_bp below.
from dashboard.analytics import analytics_bp

app.register_blueprint(analytics_bp)

# --- Monetization Tab Modularized ---
# TODO: Monetization endpoint is now in monetization.py (monetization_bp Blueprint)
# Import and register monetization_bp below.
from dashboard.monetization import monetization_bp

app.register_blueprint(monetization_bp)

# --- License Management Tab Modularized ---
# TODO: License management endpoint is now in license.py (license_bp Blueprint)
# Import and register license_bp below.
from dashboard.license import license_bp

app.register_blueprint(license_bp)

# --- Product Generation Tab Modularized ---
# TODO: Product generation endpoint is now in product_gen.py (product_gen_bp Blueprint)
# Import and register product_gen_bp below.
from dashboard.product_gen import product_gen_bp

app.register_blueprint(product_gen_bp)

# --- Reviewer Tab Modularized ---
# TODO: Reviewer analytics, escalation, training, and notification endpoints are now in reviewer.py (reviewer_bp Blueprint)
# Import and register reviewer_bp below.

# --- Accessibility Tab Modularized ---
# TODO: Accessibility audit endpoints are now in accessibility.py (accessibility_bp Blueprint)
# Import and register accessibility_bp below.
from dashboard.accessibility import accessibility_bp
from dashboard.payments import payments_bp

app.register_blueprint(payments_bp)


# --- Audit Trail Tab ---
@app.route("/audit")
@owner_required
def audit_trail():
    logs = []
    try:
        with open("../analytics/audit_trail.log") as logf:
            logs = logf.readlines()[-100:]
    except Exception:
        pass
    return render_template(
        "dashboard.html",
        content="<h3>Audit Trail</h3><pre>"
        + "".join(logs)
        + '</pre><a href="/dashboard">Back</a>',
    )


if __name__ == "__main__":
    app.run(debug=True, port=8765)
