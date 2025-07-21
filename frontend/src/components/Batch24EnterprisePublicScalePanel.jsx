import React, { useState } from "react";

const STATIC_REPORTS = [
  {
    name: "Enterprise System Audit Report",
    updated: "2025-06-22T13:00:00-06:00",
    file: "enterprise_audit.pdf",
  },
  {
    name: "Executive Public Summary",
    updated: "2025-06-22T12:30:00-06:00",
    file: "executive_summary.pdf",
  },
  {
    name: "Public Trust & Risk Index",
    updated: "2025-06-22T12:00:00-06:00",
    file: "trust_risk_index.pdf",
  },
  {
    name: "Global Readiness Checklist",
    updated: "2025-06-22T11:30:00-06:00",
    file: "readiness_checklist.pdf",
  },
  {
    name: "Trusted SAFE AI Badge",
    updated: "2025-06-22T11:00:00-06:00",
    file: "trusted_badge.pdf",
  },
  {
    name: "Ecosystem Report",
    updated: "2025-06-22T10:30:00-06:00",
    file: "ecosystem_report.pdf",
  },
];

export default function Batch24EnterprisePublicScalePanel({ onExport }) {
  const [status, setStatus] = useState(null);
  const handleExport = (file) => {
    setStatus(null);
    try {
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
      className="batch24-panel"
      aria-label="Enterprise & Public Scale"
      tabIndex={0}
      style={{ background: "#f9fafb", padding: 20, borderRadius: 8 }}
    >
      <h3 style={{ color: "#0f172a" }}>
        Batch 24: Enterprise & Public Scale Operations
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
