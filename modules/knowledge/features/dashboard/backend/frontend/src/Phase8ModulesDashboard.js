// Phase 8 SAFE AI Modules Dashboard (Wrapper)
import React from "react";
import Phase8StaticModulesPanel from "../../admin_panels/phase8_static_modules_panel";

export default function Phase8ModulesDashboard() {
  return (
    <div style={{ padding: 32 }}>
      <h1>SAFE AI Phase 8 Modules</h1>
      <Phase8StaticModulesPanel />
    </div>
  );
}
