import requests
import os
import logging

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
SERVICENOW_URL = os.getenv("SERVICENOW_URL")
SERVICENOW_USER = os.getenv("SERVICENOW_USER")
SERVICENOW_TOKEN = os.getenv("SERVICENOW_TOKEN")
ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")

logger = logging.getLogger("workflow_engine")

def trigger_compliance_workflow(event, data=None):
    # --- Jira: create ticket on failure ---
    if event == "vault_export_failed" and JIRA_URL and JIRA_USER and JIRA_TOKEN:
        requests.post(
            JIRA_URL + "/rest/api/2/issue",
            json={
                "fields": {
                    "project": {"key": "AIF"},
                    "summary": f"Vault export failed: {data.get('vault_id', 'unknown')}",
                    "description": str(data),
                    "issuetype": {"name": "Task"}
                }
            },
            auth=(JIRA_USER, JIRA_TOKEN)
        )
        logger.info("Jira ticket created.")
    # --- ServiceNow: stub ---
    if event == "vault_export_failed" and SERVICENOW_URL:
        logger.info("ServiceNow ticket logic stubbed.")
    # --- Zapier: webhook on key events ---
    if event in ["vault_created", "pdf_finalized", "price_set", "vault_uploaded"] and ZAPIER_WEBHOOK_URL:
        requests.post(ZAPIER_WEBHOOK_URL, json={"event": event, "data": data})
        logger.info(f"Zapier webhook sent: {event}")
