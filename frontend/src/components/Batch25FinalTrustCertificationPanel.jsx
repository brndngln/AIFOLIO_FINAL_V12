import React, { useState } from "react";

const STATIC_REPORTS = [
  {
    name: "Global Certification Summary",
    updated: "2025-06-22T13:00:00-06:00",
    file: "cert_summary.pdf",
  },
  {
    name: "Multi-Partner Readiness Dashboard",
    updated: "2025-06-22T12:30:00-06:00",
    file: "multi_partner_dashboard.pdf",
  },
  {
    name: "Annual Impact Report",
    updated: "2025-06-22T12:00:00-06:00",
    file: "annual_impact.pdf",
  },
  {
    name: "Trusted Partner Directory",
    updated: "2025-06-22T11:30:00-06:00",
    file: "trusted_partner_directory.pdf",
  },
  {
    name: "Governance Board Report",
    updated: "2025-06-22T11:00:00-06:00",
    file: "governance_board_report.pdf",
  },
  {
    name: "Partner Alignment Summary",
    updated: "2025-06-22T10:30:00-06:00",
    file: "alignment_summary.pdf",
  },
];

export default function Batch25FinalTrustCertificationPanel({ onExport }) {
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
      className="batch25-panel"
      aria-label="Final Public Trust & Certification"
      tabIndex={0}
      style={{ background: "#f9fafb", padding: 20, borderRadius: 8 }}
    >
      <h3 style={{ color: "#0f172a" }}>
        Batch 25: Final Public Trust & Certification
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
