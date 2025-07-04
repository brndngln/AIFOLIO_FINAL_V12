import React, { useEffect, useState } from "react";
import { runComplianceCheck } from "../../../core/audit_trail";

export default function EliteAuditComplianceDashboard({ module = "core" }) {
  const [compliance, setCompliance] = useState({});
  const [auditLog, setAuditLog] = useState([]);
  const [exportFormat, setExportFormat] = useState("json");
  const [exported, setExported] = useState("");

  useEffect(() => {
    async function fetchCompliance() {
      // Simulate API call to backend compliance check
      const result = runComplianceCheck(module);
      setCompliance(result);
    }
    fetchCompliance();
  }, [module]);

  const handleExport = async () => {
<<<<<<< HEAD
    // Simulate API call to backend export
    const { exportAudit } = await import("../../../core/audit_trail");
    setExported(exportAudit(module, exportFormat));
  };

=======
    setExported('Exporting...');
    try {
      const res = await fetch(`/api/export/audit?format=${exportFormat}`);
      if (!res.ok) throw new Error('Export failed');
      const data = (exportFormat === 'json') ? await res.json() : await res.text();
      setExported(exportFormat === 'json' ? JSON.stringify(data, null, 2) : data);
    } catch (err) {
      setExported('Export failed: ' + (err.message || err));
    }
  };


>>>>>>> omni_repair_backup_20250704_1335
  return (
    <div className="elite-audit-dashboard" style={{background:'#181e2b',color:'#b3e9ff',borderRadius:16,padding:32,boxShadow:'0 0 32px #00e6ff44'}}>
      <h2>Elite Audit & Compliance Dashboard</h2>
      <div style={{marginBottom:16}}>
        <strong>SAFE AI:</strong> {compliance.safe ? "✅" : "❌"} &nbsp;
        <strong>Privacy:</strong> {compliance.privacy ? "✅" : "❌"} &nbsp;
        <strong>Security:</strong> {compliance.security ? "✅" : "❌"}
        <span style={{marginLeft:16}}><strong>Total Events:</strong> {compliance.total}</span>
      </div>
      <div style={{marginBottom:16}}>
        <button onClick={handleExport} style={{background:'#00e6ff',color:'#181e2b',border:'none',borderRadius:8,padding:'8px 16px',fontWeight:'bold'}}>Export Audit Log</button>
        <select value={exportFormat} onChange={e => setExportFormat(e.target.value)} style={{marginLeft:8}}>
          <option value="json">JSON</option>
          <option value="csv">CSV</option>
        </select>
      </div>
      {exported && <pre style={{background:'#232b3b',color:'#00e6ff',padding:16,borderRadius:8,maxHeight:300,overflow:'auto'}}>{exported}</pre>}
      <div style={{marginTop:32,opacity:0.8}}>
        <em>All audit logs are immutable, append-only, and SAFE AI-compliant. Owner control and full transparency guaranteed.</em>
      </div>
    </div>
  );
}
