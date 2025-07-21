import React, { useState } from "react";

const STATIC_REPORTS = [
  {
    name: "Federation Alignment Report",
    updated: "2025-06-22T15:00:00-06:00",
    file: "federation_alignment.pdf",
  },
  {
    name: "Ecosystem Map",
    updated: "2025-06-22T14:00:00-06:00",
    file: "ecosystem_map.pdf",
  },
  {
    name: "Public Trust Badge",
    updated: "2025-06-22T13:00:00-06:00",
    file: "public_trust_badge.pdf",
  },
  {
    name: "Auditor Certification Export",
    updated: "2025-06-22T12:00:00-06:00",
    file: "auditor_certification.pdf",
  },
];

export default function Batch21FederatedTrustPanel({ onExport }) {
  const [status, setStatus] = useState(null);

  const handleExport = (file) => {
    setStatus(null);
    // Simulate export, always owner-triggered
    try {
      // In real code, call backend API here
      setTimeout(() => {
        setStatus({
          type: "success",
          msg: `Exported ${file} (manual, audit-logged)`,
        });
        if (onExport) onExport(file);
      }, 500);
    } catch (e) {
      setStatus({ type: "error", msg: `Failed to export ${file}` });
    }
  };

  return (
    <div
      className="batch21-panel"
      aria-label="Federated Trust & Governance"
      tabIndex={0}
      style={{ background: "#f9fafb", padding: 20, borderRadius: 8 }}
    >
      <h3 style={{ color: "#0f172a" }}>
        Batch 21: Federated Trust & Governance
      </h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {STATIC_REPORTS.map((rep) => (
          <li
            key={rep.file}
            style={{
              marginBottom: 12,
              background: "#fff",
              padding: 10,
              borderRadius: 6,
              boxShadow: "0 1px 2px #e2e8f0",
            }}
          >
            <b>{rep.name}</b>{" "}
            <span style={{ color: "#64748b", fontSize: 13 }}>
              Last updated: {rep.updated}
            </span>
            <button
              style={{
                marginLeft: 16,
                background: "#2563eb",
                color: "#fff",
                border: "none",
                borderRadius: 4,
                padding: "4px 12px",
              }}
              onClick={() => handleExport(rep.file)}
            >
              Export PDF
            </button>
          </li>
        ))}
      </ul>
      {status && (
        <div
          style={{
            marginTop: 10,
            color: status.type === "success" ? "#059669" : "#dc2626",
            fontWeight: 500,
          }}
        >
          {status.msg}
        </div>
      )}
      <div style={{ marginTop: 16, fontSize: 13, color: "#64748b" }}>
        All exports are owner-triggered, static, and audit-logged. No
        public/partner export unless you manually approve.
      </div>
    </div>
  );
}
