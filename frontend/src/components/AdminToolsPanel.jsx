import React, { useState } from "react";
import AuditLogViewer from "./AuditLogViewer";
import HyperEliteVaultBadge from "../../components/HyperEliteVaultBadge";
import ExportHistoryPanel from "./ExportHistoryPanel";
import UserManagementPanel from "./UserManagementPanel";
import AdminSessionPanel from "./AdminSessionPanel";
import AdminSettingsPanel from "./AdminSettingsPanel";

const TABS = [
  { key: "audit", label: "Audit Log" },
  { key: "export", label: "Export History" },
  { key: "users", label: "User Management" },
  { key: "sessions", label: "Sessions" },
  { key: "settings", label: "SAFE AI Settings" },
];

export default function AdminToolsPanel({ token }) {
  const [tab, setTab] = useState("audit");
  return (
    <section
      className="admin-tools-panel"
      aria-label="Admin Tools"
      style={{
        marginTop: 32,
        background: "rgba(255,255,255,0.72)",
        padding: 32,
        borderRadius: 24,
        boxShadow: "0 4px 32px #b6e3e0a0",
        fontFamily: "Inter, SF Pro Display, Arial, sans-serif",
        maxWidth: 1000,
        marginLeft: "auto",
        marginRight: "auto",
        backdropFilter: "blur(5px)",
      }}
    >
      <h2
        style={{
          color: "#1e293b",
          fontWeight: 800,
          fontSize: 32,
          marginBottom: 20,
          display: "flex",
          alignItems: "center",
          gap: 10,
          letterSpacing: "0.01em",
          textShadow: "0 2px 12px #e3f9f6",
        }}
      >
        Admin Tools
        <HyperEliteVaultBadge tooltip={true} external={false} />
      </h2>
      {/* Auto-Repair Daemon Status Widget */}
      <div
        aria-label="Auto-Repair Daemon Status"
        style={{
          background: "rgba(12,131,124,0.08)",
          borderRadius: 12,
          padding: "1.2em 2em",
          marginBottom: 24,
          display: "flex",
          alignItems: "center",
          gap: 18,
          fontWeight: 600,
          fontSize: 18,
          color: "#0c837c",
          boxShadow: "0 1px 8px #b6e3e044",
        }}
      >
        <span
          style={{
            fontWeight: 800,
            fontSize: 20,
            color: "#0c837c",
            marginRight: 8,
          }}
        >
          Auto-Repair Daemon
        </span>
        <span
          style={{
            background: "#e3f9f6",
            color: "#0c837c",
            borderRadius: 8,
            padding: "0.3em 1em",
            fontWeight: 700,
            fontSize: 17,
          }}
        >
          Operational
        </span>
        <span style={{ marginLeft: 16, color: "#888", fontSize: 15 }}>
          All monitored services healthy. Last escalation: None.
        </span>
        <button
          aria-label="Escalate Issue"
          style={{
            marginLeft: "auto",
            background: "#e53e3e",
            color: "#fff",
            border: "none",
            borderRadius: 7,
            padding: "0.5em 1.2em",
            fontWeight: 700,
            cursor: "pointer",
            fontSize: 15,
            boxShadow: "0 1px 4px #e53e3e33",
          }}
          onClick={() => alert("Escalation triggered. SAFE AI audit logged.")}
        >
          Escalate
        </button>
      </div>
      <nav
        aria-label="Admin Tool Tabs"
        style={{
          marginBottom: 24,
          display: "flex",
          gap: 10,
          background: "rgba(227,249,246,0.7)",
          borderRadius: 8,
          padding: "0.5em 0.5em",
          boxShadow: "0 1px 6px #e3f9f6",
        }}
      >
        {TABS.map((t) => (
          <button
            key={t.key}
            aria-label={t.label}
            onClick={() => setTab(t.key)}
            style={{
              padding: "10px 24px",
              border: "none",
              borderRadius: 8,
              background: tab === t.key ? "#0c837c" : "rgba(255,255,255,0.92)",
              color: tab === t.key ? "#fff" : "#1e293b",
              fontWeight: 700,
              fontSize: 16,
              cursor: "pointer",
              outline: tab === t.key ? "2px solid #0c837c" : "none",
              boxShadow: tab === t.key ? "0 2px 8px #dbeafe" : "none",
              transition: "all 0.2s cubic-bezier(.4,2,.6,1)",
            }}
          >
            {t.label}
          </button>
        ))}
      </nav>
      <div
        style={{
          background: "rgba(255,255,255,0.93)",
          padding: 28,
          borderRadius: 14,
          boxShadow: "0 2px 18px #e5e7eb",
          minHeight: 320,
          marginTop: 2,
        }}
      >
        {tab === "audit" && <AuditLogViewer token={token} showDownload />}
        {tab === "export" && <ExportHistoryPanel token={token} showDownload />}
        {tab === "users" && <UserManagementPanel token={token} enableRoles />}
        {tab === "sessions" && <AdminSessionPanel />}
        {tab === "settings" && <AdminSettingsPanel />}
      </div>
    </section>
  );
}
