import React from "react";

export default function AdminSettingsPanel() {
  return (
    <div className="admin-settings-panel" aria-label="SAFE AI Settings" tabIndex={0} style={{background:'#f3f4f6',padding:20,borderRadius:8}}>
      <h3 style={{color:'#0f172a'}}>SAFE AI Compliance Settings</h3>
      <ul style={{listStyle:'none',padding:0}}>
        <li><b>SAFE AI Mode:</b> <span style={{color:'#059669'}}>ENABLED</span></li>
        <li><b>Audit Logging:</b> <span style={{color:'#059669'}}>ENABLED</span></li>
        <li><b>Static UI Feedback:</b> <span style={{color:'#059669'}}>ENABLED</span></li>
        <li><b>Adaptive/Agentic UI:</b> <span style={{color:'#ef4444'}}>DISABLED</span></li>
        <li><b>Data Export Logging:</b> <span style={{color:'#059669'}}>ENABLED</span></li>
        <li><b>Partner/Public Export:</b> <span style={{color:'#059669'}}>ENABLED</span></li>
      </ul>
      <div style={{marginTop:12,fontSize:13,color:'#64748b'}}>
        All settings are static, deterministic, and SAFE AI compliant. No adaptive or agentic behavior is enabled.
      </div>
    </div>
  );
}
