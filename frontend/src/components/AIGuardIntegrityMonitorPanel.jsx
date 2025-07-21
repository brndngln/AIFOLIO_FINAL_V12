import React from "react";

export default function AIGuardIntegrityMonitorPanel() {
  return (
    <section
      aria-labelledby="ai-guard-integrity-heading"
      style={{
        background: "#f3f4f6",
        borderRadius: 12,
        padding: 24,
        marginBottom: 24,
        boxShadow: "0 1px 4px #cbd5e1",
      }}
    >
      <h3
        id="ai-guard-integrity-heading"
        style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 10 }}
      >
        AI Guard Integrity Monitor
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        <li>
          Static monitor to ensure no sentient/adaptive/recursive AI logic
          enters SAFE AI core
        </li>
        <li>OWNER can review integrity status and logs</li>
        <li>All logic is static, deterministic, and OWNER-controlled</li>
      </ul>
    </section>
  );
}
