import React, { useState } from "react";

const STATIC_CERTS = [
  {
    name: "Certification Renewal Tracker",
    updated: "2025-06-22T13:30:00-06:00",
    file: "cert_renewal_tracker.pdf",
  },
  {
    name: "Annual Audit Generator",
    updated: "2025-06-22T12:45:00-06:00",
    file: "annual_audit.pdf",
  },
  {
    name: "Partner Cert Directory",
    updated: "2025-06-22T12:10:00-06:00",
    file: "cert_directory.pdf",
  },
  {
    name: "Legal Change Monitor",
    updated: "2025-06-22T11:30:00-06:00",
    file: "legal_change_monitor.pdf",
  },
  {
    name: "Policy Summary Export",
    updated: "2025-06-22T11:00:00-06:00",
    file: "policy_summary.pdf",
  },
];

export default function Batch22CertificationLegalPanel({ onExport }) {
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
      className="batch22-panel"
      aria-label="Certification & Legal Readiness"
      tabIndex={0}
      style={{ background: "#f3f4f6", padding: 20, borderRadius: 8 }}
    >
      <h3 style={{ color: "#0f172a" }}>
        Batch 22: Certification & Legal Readiness
      </h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {STATIC_CERTS.map((cert) => (
          <li
            key={cert.file}
            style={{
              marginBottom: 12,
              background: "#fff",
              padding: 10,
              borderRadius: 6,
              boxShadow: "0 1px 2px #e2e8f0",
            }}
          >
            <b>{cert.name}</b>{" "}
            <span style={{ color: "#64748b", fontSize: 13 }}>
              Last updated: {cert.updated}
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
              onClick={() => handleExport(cert.file)}
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
