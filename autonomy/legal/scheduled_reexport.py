import time
from autonomy.legal.legal_export import export_all_policies_as_pdf


def scheduled_policy_reexport(interval_hours=168):
    """
    Re-export all policy PDFs on a fixed schedule (default: weekly).
    """
    while True:
        export_all_policies_as_pdf("../../distribution/legal_exports/")
        time.sleep(interval_hours * 3600)
