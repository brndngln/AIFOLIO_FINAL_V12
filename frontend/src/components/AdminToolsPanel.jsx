import React, { useState } from "react";
import AuditLogViewer from "./AuditLogViewer";
import HyperEliteVaultBadge from '../../components/HyperEliteVaultBadge';
import ExportHistoryPanel from "./ExportHistoryPanel";
import UserManagementPanel from "./UserManagementPanel";
import AdminSessionPanel from "./AdminSessionPanel";
import AdminSettingsPanel from "./AdminSettingsPanel";

const TABS = [
  { key: "audit", label: "Audit Log" },
  { key: "export", label: "Export History" },
  { key: "users", label: "User Management" },
  { key: "sessions", label: "Sessions" },
  { key: "settings", label: "SAFE AI Settings" }
];

export default function AdminToolsPanel({ token }) {
  const [tab, setTab] = useState("audit");
  return (
    <section className="admin-tools-panel" aria-label="Admin Tools" style={{marginTop:32,background:'#f3f4f6',padding:24,borderRadius:12}}>
      <h2 style={{color:'#1e293b',fontWeight:700,fontSize:28,marginBottom:16,display:'flex',alignItems:'center',gap:8}}>
  Admin Tools
  <HyperEliteVaultBadge tooltip={true} external={false} />
</h2>
      <nav aria-label="Admin Tool Tabs" style={{marginBottom:24,display:'flex',gap:8}}>
        {TABS.map(t => (
          <button
            key={t.key}
            aria-label={t.label}
            onClick={() => setTab(t.key)}
            style={{
              padding:'8px 18px',
              border:'none',
              borderRadius:6,
              background: tab===t.key ? '#2563eb' : '#e5e7eb',
              color: tab===t.key ? '#fff' : '#1e293b',
              fontWeight:600,
              cursor:'pointer',
              outline: tab===t.key ? '2px solid #2563eb' : 'none',
              boxShadow: tab===t.key ? '0 2px 8px #dbeafe' : 'none'
            }}
          >{t.label}</button>
        ))}
      </nav>
      <div style={{background:'#fff',padding:24,borderRadius:10,boxShadow:'0 2px 8px #e5e7eb',minHeight:320}}>
        {tab === "audit" && <AuditLogViewer token={token} showDownload />}
        {tab === "export" && <ExportHistoryPanel token={token} showDownload />}
        {tab === "users" && <UserManagementPanel token={token} enableRoles />}
        {tab === "sessions" && <AdminSessionPanel />}
        {tab === "settings" && <AdminSettingsPanel />}
      </div>
    </section>
  );
}
