import React from "react";

// [WINDSURF FIXED ✅]
export default function ComplianceWorkflowStack() {
  return (
    <div
      style={{
        marginTop: 32,
        background: "#f9fafb",
        borderRadius: 8,
        padding: 24,
        boxShadow: "0 1px 3px #e5e7eb",
      }}
    >
      <h3 style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 12 }}>
        COMPLIANCE & WORKFLOW STACK
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        <li>✔️ Tax Engine (TaxJar, Avalara, VATLayer)</li>
        <li>✔️ Alerts (SendGrid, Twilio, Slack/Discord)</li>
        <li>✔️ E-Filing Engine (IRS, HMRC, EU, India)</li>
        <li>✔️ Workflow Automation (Jira, Zapier, ServiceNow)</li>
        <li>✔️ Compliance Export Engine (PDF, CSV, XBRL)</li>
      </ul>
    </div>
  );
}
