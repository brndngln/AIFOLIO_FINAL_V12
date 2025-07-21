import React from "react";

const FEATURES = [
  "AI Market Predictor 5+ Years",
  "AI Human Capital Engine",
  "AI Content Evolution Engine",
  "AI Governance Enforcer",
  "AI Regulatory Watchdog",
  "Planetary Scaling Engine",
  "AI Hyper-Scaling Mode",
];

export default function Phase4000SelectedStatusPanel() {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.82)",
        borderRadius: "2em",
        boxShadow: "0 6px 32px #b6e3e0a0",
        padding: "2.5em 2em",
        margin: "2em 0",
        fontFamily: "Inter, SF Pro Display, Arial, sans-serif",
        color: "#1a1a1a",
        maxWidth: 900,
        marginLeft: "auto",
        marginRight: "auto",
        border: "1.5px solid #e3f9f6",
      }}
    >
      <h2
        style={{
          fontWeight: 800,
          fontSize: "2.2em",
          marginBottom: "0.4em",
          color: "#0c837c",
          letterSpacing: "0.01em",
        }}
      >
        AIFOLIO™ EMPIRE PHASE 4000+ SELECTED STATUS
      </h2>
      <ul
        style={{
          fontSize: "1.19em",
          lineHeight: 1.7,
          paddingLeft: 28,
          margin: 0,
        }}
      >
        {FEATURES.map((feature) => (
          <li key={feature}>
            <b>{feature}</b>{" "}
            <span style={{ color: "#0c837c", fontWeight: 700 }}>&#10003;</span>
          </li>
        ))}
      </ul>
      <div
        style={{
          marginTop: "1.6em",
          fontSize: "1.1em",
          color: "#2563eb",
          fontWeight: 600,
        }}
      >
        <a
          href="/analytics/phase_4000_selected_status.json"
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Phase 4000+ Selected Status (JSON)
        </a>
        <span style={{ margin: "0 1em" }}>|</span>
        <a
          href="/analytics/phase_4000_selected_status.csv"
          target="_blank"
          rel="noopener noreferrer"
        >
          Download Phase 4000+ Selected Status (CSV)
        </a>
      </div>
      <div
        style={{
          marginTop: "2em",
          fontSize: "1.05em",
          background: "#e3f9f6",
          borderRadius: "1em",
          padding: "1.2em 1.5em",
          color: "#0c837c",
          fontWeight: 700,
        }}
      >
        <span>
          SAFE AI GOVERNANCE: <b>ENFORCED</b> — ONLY APPROVED PHASE 4000+
          FEATURES IMPLEMENTED — SOVEREIGN, AUTONOMOUS, GLOBALLY SCALED
        </span>
      </div>
      <div style={{ marginTop: "1.4em", textAlign: "right" }}>
        <span
          style={{
            display: "inline-block",
            padding: "0.25em 0.7em",
            borderRadius: "1em",
            background: "#e3f9f6",
            color: "#0c837c",
            fontSize: "1em",
            fontWeight: 700,
            letterSpacing: "0.03em",
          }}
        >
          PHASE 4000+ SELECTED — FINAL STATE
        </span>
      </div>
    </div>
  );
}
