import React, { useState } from "react";
import AuditLogPanel from "./AuditLogPanel";
import CompletionChecklist from "./CompletionChecklist";
import ReadinessChecklist from "./ReadinessChecklist";
import UXBestPractices from "./UXBestPractices";
import GlobalPartnershipPlaybook from "./GlobalPartnershipPlaybook";

export default function OwnerControlPanel({
  auditLog,
  onExport,
  onChecklistExport,
}) {
  return (
    <div style={{ padding: 32, background: "#f3f4f6", borderRadius: 12 }}>
      <h2
        style={{
          color: "#2563eb",
          fontWeight: 700,
          fontSize: 28,
          marginBottom: 16,
        }}
      >
        AIFOLIO OWNER CONTROL PANEL
      </h2>
      <div style={{ marginBottom: 24 }}>
        <button
          onClick={onExport}
          style={{
            background: "#2563eb",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            padding: "10px 24px",
            fontWeight: 600,
            marginRight: 12,
          }}
        >
          Export All AIFOLIO Reports
        </button>
        <button
          onClick={onChecklistExport}
          style={{
            background: "#059669",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            padding: "10px 24px",
            fontWeight: 600,
          }}
        >
          Export AIFOLIO Completion Checklist
        </button>
      </div>
      <AuditLogPanel auditLog={auditLog} />
      <CompletionChecklist />
      <ReadinessChecklist />
      <UXBestPractices />
      <GlobalPartnershipPlaybook />
    </div>
  );
}
