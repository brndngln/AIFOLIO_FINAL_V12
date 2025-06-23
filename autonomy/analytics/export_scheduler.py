"""
AIFOLIO SAFE AI Export Scheduler
- Schedules weekly/monthly PDF+email exports (revenue, compliance)
- Uses SendGrid for email
- Logs all export runs to analytics_log.json
- No table-driven logic, admin reviewed only
"""
import os
import json
import schedule
import time
from datetime import datetime
# import sendgrid
# from sendgrid.helpers.mail import Mail

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'analytics_log.json'))

# Placeholder for SendGrid API
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'YOUR_SENDGRID_API_KEY')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')


def send_email(subject, body, attachment_path=None):
    # Stub: integrate with SendGrid
    # sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    # ...
    print(f"Email sent to {ADMIN_EMAIL}: {subject}")


def export_and_email(report_type, static_range, stats):
    output_path = f"/tmp/{report_type}_report_{static_range.replace(' ', '_')}.pdf"
    # generate_revenue_report_pdf(static_range, output_path, stats)  # or compliance report
    send_email(f"AIFOLIO {report_type.title()} Report", f"Report for {static_range}", output_path)
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps({'action': 'export_email', 'report_type': report_type, 'static_range': static_range, 'timestamp': datetime.utcnow().isoformat()}) + '\n')


def schedule_exports():
    schedule.every().monday.at("08:00").do(export_and_email, 'revenue', 'last week', {})
    schedule.every().month.at("08:00").do(export_and_email, 'compliance', 'last month', {})
    while True:
        schedule.run_pending()
        time.sleep(60)

# To run: schedule_exports()
