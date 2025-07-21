import React, { useState } from "react";
import axios from "axios";

const automations = [
  {
    label: "Generate Vault",
    endpoint: "/api/generate-vault",
    method: "POST",
    body: { topic: "Demo Niche" },
  },
  {
    label: "Refresh Analytics",
    endpoint: "/api/analytics/metrics",
    method: "GET",
  },
  {
    label: "Run Compliance Check",
    endpoint: "/api/monitor/metrics",
    method: "GET",
  },
];

const AutomationTriggerPanel = () => {
  const [status, setStatus] = useState({});

  const triggerAutomation = async (automation) => {
    setStatus((s) => ({ ...s, [automation.label]: "Running..." }));
    try {
      const token = localStorage.getItem("token");
      let res;
      if (automation.method === "POST") {
        res = await axios.post(automation.endpoint, automation.body, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        res = await axios.get(automation.endpoint, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      setStatus((s) => ({ ...s, [automation.label]: "Success!" }));
    } catch (err) {
      setStatus((s) => ({ ...s, [automation.label]: "Error!" }));
    }
  };

  return (
    <div
      className="theme-card"
      style={{
        background: "var(--background)",
        color: "var(--text)",
        boxShadow: "var(--shadow-md)",
        borderRadius: "var(--border-radius-lg)",
        padding: "2rem",
        marginBottom: "2rem",
      }}
    >
      <h3 style={{ color: "var(--accent)" }}>Automation Triggers</h3>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          marginTop: "1.5rem",
        }}
      >
        {automations.map((auto) => (
          <button
            key={auto.label}
            className="btn-matte"
            style={{
              background: "var(--cta)",
              color: "var(--background)",
              borderRadius: "8px",
              padding: "0.75rem 1.5rem",
              fontWeight: 600,
              fontSize: "1.1rem",
              boxShadow: "var(--shadow-xs)",
              border: "none",
              cursor: "pointer",
              transition: "background 0.2s",
            }}
            onClick={() => triggerAutomation(auto)}
          >
            {auto.label}
          </button>
        ))}
      </div>
      <div
        style={{
          marginTop: "1.5rem",
          fontSize: "1rem",
          color: "var(--secondary)",
        }}
      >
        {Object.entries(status).map(([label, stat]) => (
          <div key={label}>
            {label}: <span style={{ fontWeight: 600 }}>{stat}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AutomationTriggerPanel;
