import React, { useState } from "react";

const initialAutomations = [
  { id: 1, trigger: "vault_exported", action: "Send Email", enabled: true },
  { id: 2, trigger: "vault_published", action: "Notify Slack", enabled: false },
];

export default function AutomationBuilder() {
  const [automations, setAutomations] = useState(initialAutomations);
  const addAutomation = () =>
    setAutomations([
      ...automations,
      { id: Date.now(), trigger: "", action: "", enabled: true },
    ]);

  return (
    <div
      className="automation-builder"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
      }}
    >
      <h2>No-Code Automation Builder</h2>
      <table style={{ width: "100%", background: "#232b3b", borderRadius: 8 }}>
        <thead>
          <tr style={{ color: "#00e6ff" }}>
            <th>Trigger</th>
            <th>Action</th>
            <th>Enabled</th>
          </tr>
        </thead>
        <tbody>
          {automations.map((a) => (
            <tr key={a.id}>
              <td>{a.trigger}</td>
              <td>{a.action}</td>
              <td>
                <input type="checkbox" checked={a.enabled} readOnly />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        onClick={addAutomation}
        style={{
          background: "#00e6ff",
          color: "#181e2b",
          border: "none",
          borderRadius: 8,
          padding: "8px 16px",
          fontWeight: "bold",
          marginTop: 16,
        }}
      >
        Add Automation
      </button>
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          Connect vault events to external services (Email, Slack, Discord,
          Google Drive, Notion, etc). All automations are owner-controlled and
          SAFE AI-compliant.
        </em>
      </div>
    </div>
  );
}
