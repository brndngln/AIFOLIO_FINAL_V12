// OMNIELITE AIFOLIO - Audit Trail Export Panel (React)
// Surfaces audit exports for owner review, export, and compliance
import React, { useState } from 'react';

function AuditTrailExportPanel() {
  const [module, setModule] = useState('vault_registry');
  const [format, setFormat] = useState('json');
  const [auditData, setAuditData] = useState('');

  const fetchAudit = async () => {
    // This would call a backend API endpoint in production
    try {
      const res = await fetch(`/api/audit/export?module=${module}&format=${format}`);
      const data = await res.text();
      setAuditData(data);
    } catch (e) {
      setAuditData('Error loading audit data.');
    }
  };

  return (
    <div className="audit-panel">
      <h2>Audit Trail Export</h2>
      <div>
        <label>Module: </label>
        <input value={module} onChange={e => setModule(e.target.value)} />
        <label>Format: </label>
        <select value={format} onChange={e => setFormat(e.target.value)}>
          <option value="json">JSON</option>
          <option value="csv">CSV</option>
        </select>
        <button onClick={fetchAudit}>Export</button>
      </div>
      <textarea value={auditData} readOnly rows={10} style={{ width: '100%', marginTop: 10 }} />
    </div>
  );
}

// [WINDSURF FIXED ✅]
export default AuditTrailExportPanel;
