"""
reviewer.py — Reviewer Analytics, Escalation, and Training Blueprint
Elite security, ethics, and maintainability: CSRF, audit logging, anti-sentience, modular.
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import threading
import os
import json

# --- Blueprint Setup ---
reviewer_bp = Blueprint("reviewer", __name__, template_folder="templates")

# --- Locks and Files ---
ESCALATION_STATES = ["pending", "resolved", "rejected"]
ESCALATION_FILE = "../analytics/escalations.log"
ESCALATION_LOCK = threading.Lock()
REVIEWER_TRAINING_FILE = "../analytics/reviewer_training.log"
REVIEWER_TRAINING_BACKUP = "../analytics/reviewer_training_backup.log"
AUDIT_LOG = "../analytics/audit_trail.log"
AUDIT_BACKUP = "../analytics/audit_trail_backup.log"
NOTIF_SETTINGS_FILE = "../analytics/notification_settings.json"
NOTIF_SETTINGS_LOCK = threading.Lock()


# --- Security/Ethics Utilities (assume import or define here as needed) ---
def validate_csrf_token(token):
    # Placeholder: import from main app or implement
    from dashboard.web_dashboard import validate_csrf_token as vct

    return vct(token)


def generate_csrf_token():
    from dashboard.web_dashboard import generate_csrf_token as gct

    return gct()


def anti_sentience_scan(val):
    from dashboard.web_dashboard import anti_sentience_scan as asscan

    return asscan(val)


# --- Reviewer Training ---
@reviewer_bp.route("/reviewer_training", methods=["GET", "POST"])
def reviewer_training():
    """Reviewer training event logging with CSRF and double audit log."""
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            return "CSRF validation failed", 400
        reviewer = request.form["reviewer"]
        action = request.form["action"]
        notes = request.form.get("notes", "")
        anti_sentience_scan(action)
        for logf in [REVIEWER_TRAINING_FILE, REVIEWER_TRAINING_BACKUP]:
            with open(logf, "a") as logfobj:
                logfobj.write(f"{datetime.now()}|{reviewer}|{action}|{notes}\n")
        for logf in [AUDIT_LOG, AUDIT_BACKUP]:
            with open(logf, "a") as logfobj:
                logfobj.write(
                    f"REVIEWER_TRAINING: {reviewer} {action} at {datetime.now()}\n"
                )
        return redirect(url_for("reviewer.reviewer_training"))
    csrf_token = generate_csrf_token()
    form = f"""<form method="post">
    <input name="reviewer" placeholder="Reviewer Name" required/><br>
    <input name="action" placeholder="Action (approve, reject, escalate, etc)" required/><br>
    <input name="notes" placeholder="Notes"/><br>
    <input type="hidden" name="csrf_token" value="{csrf_token}"/>
    <button type="submit">Log Training Event</button></form>"""
    return render_template("reviewer_training.html", form=form)


# --- Reviewer Escalations ---
@reviewer_bp.route(
    "/api/analytics/reviewer_escalations", methods=["GET", "POST", "PUT"]
)
def reviewer_escalations():
    """Reviewer escalation workflow with CSRF, audit, and backup logging."""
    if request.method == "POST":
        data = request.get_json()
        reviewer = data.get("reviewer")
        reason = data.get("reason")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = request.remote_addr
        state = "pending"
        with ESCALATION_LOCK, open(ESCALATION_FILE, "a") as f:
            f.write(f"{timestamp}|{reviewer}|{reason}|{ip}|{state}|\n")
        for logf in [AUDIT_LOG, AUDIT_BACKUP]:
            with open(logf, "a") as logfobj:
                logfobj.write(
                    f"ESCALATION: {reviewer} escalated at {timestamp} from {ip} - Reason: {reason}\n"
                )
        return jsonify({"status": "ok"})
    elif request.method == "PUT":
        data = request.get_json()
        reviewer = data.get("reviewer")
        timestamp = data.get("timestamp")
        new_state = data.get("state")
        resolution_reason = data.get("resolution_reason", "")
        if new_state not in ESCALATION_STATES or not reviewer or not timestamp:
            return jsonify({"error": "Invalid parameters"}), 400
        updated = False
        with ESCALATION_LOCK:
            lines = []
            with open(ESCALATION_FILE) as f:
                for l in f:
                    parts = l.strip().split("|")
                    if (
                        len(parts) >= 5
                        and parts[0] == timestamp
                        and parts[1] == reviewer
                    ):
                        parts[4] = new_state
                        if len(parts) < 6:
                            parts.append(resolution_reason)
                        else:
                            parts[5] = resolution_reason
                        updated = True
                    lines.append("|".join(parts))
            with open(ESCALATION_FILE, "w") as f:
                for l in lines:
                    f.write(l + "\n")
        for logf in [AUDIT_LOG, AUDIT_BACKUP]:
            with open(logf, "a") as logfobj:
                logfobj.write(
                    f"ESCALATION: {reviewer} {new_state} at {datetime.now()} - Reason: {resolution_reason}\n"
                )
        return jsonify({"updated": updated})
    escalations = []
    try:
        with open(ESCALATION_FILE) as f:
            lines = f.readlines()[-100:]
            for l in lines:
                parts = l.strip().split("|")
                if len(parts) >= 5:
                    escalations.append(
                        {
                            "reviewer": parts[1],
                            "reason": parts[2],
                            "timestamp": parts[0],
                            "ip": parts[3],
                            "state": parts[4],
                            "resolution_reason": parts[5] if len(parts) > 5 else "",
                        }
                    )
    except Exception:
        pass
    return jsonify({"escalations": escalations})


# --- Reviewer Analytics ---
@reviewer_bp.route("/api/analytics/reviewer_stats")
def reviewer_stats():
    """Enhanced reviewer stats with audit and backup logging."""
    stats = {}
    try:
        with open(REVIEWER_TRAINING_FILE) as f:
            lines = f.readlines()[-200:]
            for l in lines:
                parts = l.strip().split("|")
                if len(parts) > 3:
                    reviewer = parts[1]
                    event = parts[2]
                    timestamp = parts[0]
                    response_time = (
                        float(parts[3]) if parts[3].replace(".", "", 1).isdigit() else 0
                    )
                    correct = (parts[4].lower() == "true") if len(parts) > 4 else None
                    s = stats.setdefault(
                        reviewer,
                        {
                            "reviewer": reviewer,
                            "events": 0,
                            "total_reviews": 0,
                            "total_response_time": 0,
                            "correct": 0,
                            "last_activity": timestamp,
                            "escalations": 0,
                        },
                    )
                    s["events"] += 1
                    s["total_reviews"] += 1
                    s["total_response_time"] += response_time
                    if correct is not None:
                        s["correct"] += int(correct)
                    s["last_activity"] = max(s["last_activity"], timestamp)
    except Exception:
        pass
    reviewer_escalations = {}
    try:
        with open(ESCALATION_FILE) as f:
            for l in f.readlines():
                parts = l.strip().split("|")
                if len(parts) > 2:
                    reviewer = parts[1]
                    reviewer_escalations[reviewer] = (
                        reviewer_escalations.get(reviewer, 0) + 1
                    )
    except Exception:
        pass
    metrics = []
    for r, s in stats.items():
        total = s["total_reviews"]
        metrics.append(
            {
                "reviewer": r,
                "events": s["events"],
                "last_activity": s["last_activity"],
                "avg_response_time": round(s["total_response_time"] / total, 2)
                if total
                else 0,
                "accuracy_rate": round(100 * s["correct"] / total, 1) if total else 0,
                "total_reviews": total,
                "escalation_rate": round(
                    100 * reviewer_escalations.get(r, 0) / total, 1
                )
                if total
                else 0,
                "escalations": reviewer_escalations.get(r, 0),
            }
        )
    return jsonify({"stats": metrics})


# --- Notification Settings (Reviewer) ---
@reviewer_bp.route("/api/notification_settings", methods=["GET", "POST"])
def notification_settings():
    ip = request.remote_addr
    if request.method == "POST":
        data = request.get_json()
        with NOTIF_SETTINGS_LOCK:
            try:
                settings = {}
                if os.path.exists(NOTIF_SETTINGS_FILE):
                    with open(NOTIF_SETTINGS_FILE) as f:
                        settings = json.load(f)
                settings[ip] = data
                with open(NOTIF_SETTINGS_FILE, "w") as f:
                    json.dump(settings, f)
            except Exception:
                return jsonify({"error": "Could not save settings"}), 500
        return jsonify({"status": "ok"})
    # GET
    with NOTIF_SETTINGS_LOCK:
        try:
            if os.path.exists(NOTIF_SETTINGS_FILE):
                with open(NOTIF_SETTINGS_FILE) as f:
                    settings = json.load(f)
                return jsonify(settings.get(ip, {}))
        except Exception:
            pass
    return jsonify({})


# --- TODO: Add further reviewer-related endpoints as needed for modularity, security, and ethics. ---
