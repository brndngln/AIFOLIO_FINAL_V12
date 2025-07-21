import React from "react";

const DASHBOARD_ITEMS = [
  "SAFE AI Government Agency Policy Map",
  "Public Global Agency Certification Alignment Report",
  "Global Public Agency SAFE AI Dashboard",
  "SAFE AI Multi-Region Policy Crosswalk",
  "Public SAFE AI World Report Generator",
  "Cross-National SAFE AI Public Governance Index",
  "Annual SAFE AI World Leadership Public Summary",
  "SAFE AI Global Partnership Alignment Tracker",
  "SAFE AI Public-Private Governance Board Export",
  "World Trust & Transparency Dashboard (OWNER controlled)",
];

export default function WorldTrustDashboard() {
  return (
    <div
      style={{
        marginTop: 32,
        background: "#fff",
        borderRadius: 8,
        padding: 24,
        boxShadow: "0 1px 3px #e5e7eb",
      }}
    >
      <h3 style={{ color: "#059669", fontWeight: 700, marginBottom: 12 }}>
        World Trust & Transparency Dashboard
      </h3>
      <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
        {DASHBOARD_ITEMS.map((item, i) => (
          <li key={i} style={{ marginBottom: 8 }}>
            <span style={{ color: "#059669", fontWeight: 600 }}>✔</span> {item}
          </li>
        ))}
      </ul>
      <div style={{ marginTop: 18, color: "#64748b", fontSize: 13 }}>
        <b>OWNER CONTROLLED:</b> No auto-publicity, no adaptive dashboards, all
        reports static and exportable only by OWNER.
      </div>
    </div>
  );
}
