// Phase 9+ SAFE AI Empire Modules Dashboard (Wrapper)
import React from "react";
import Phase9StaticModulesPanel from "../../admin_panels/phase9_static_modules_panel";
import Phase9AuditLogWidget from "./components/Phase9AuditLogWidget";
import Phase9KeyAdminPanel from "./components/Phase9KeyAdminPanel";
import Phase9AuditLogStream from "./components/Phase9AuditLogStream";
import StaticEnhancementsPanel from "./components/StaticEnhancementsPanel"; // Added: Static future enhancements panel

export default function Phase9ModulesDashboard() {
  return (
    <div style={{ padding: 32 }}>
      <h1>SAFE AI Phase 9+ Empire Modules</h1>
      <Phase9KeyAdminPanel />
      <Phase9AuditLogStream />
      <Phase9AuditLogWidget />
      <Phase9StaticModulesPanel />
      {/* Static Future Enhancements Panel */}
      <StaticEnhancementsPanel
        apiBase="http://localhost:PORT"
        tenantId={"default_tenant"}
      />
    </div>
  );
}
