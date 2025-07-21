// OMNIELITE AIFOLIO - Admin Audit Dashboard (React)
// Surfaces audit logs, compliance status, and export for owner review
import React, { useState } from "react";
import AuditTrailExportPanel from "../components/AuditTrailExportPanel";

function AdminAuditDashboard() {
  const [selectedModule, setSelectedModule] = useState("vault_registry");

  return (
    <div className="admin-audit-dashboard">
      <h1>Admin Audit Dashboard</h1>
      <div style={{ marginBottom: 24 }}>
        <strong>Compliance Status:</strong> All workflows and modules are
        static, deterministic, SAFE AI-compliant, and fully auditable.
      </div>
      <AuditTrailExportPanel />
      <div style={{ marginTop: 32 }}>
        <h3>Instructions</h3>
        <ul>
          <li>
            Use the export panel to review or download audit logs for any
            module.
          </li>
          <li>
            Ensure all business-critical workflows are logged and regularly
            reviewed for compliance.
          </li>
          <li>
            All exports are static, owner-controlled, and SAFE AI-compliant.
          </li>
        </ul>
      </div>
    </div>
  );
}

export default AdminAuditDashboard;
