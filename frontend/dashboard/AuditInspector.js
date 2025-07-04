// AIFOLIO SAFE AI Audit Inspector Component
// Allows admin to inspect all analytics, compliance, and pipeline logs
import React, { useEffect, useState } from 'react';
import { fetchAdminAuditInspect } from './api';

export default function AuditInspector() {
  const [audit, setAudit] = useState('');
  useEffect(() => {
    fetchAdminAuditInspect().then(data => setAudit(JSON.stringify(data, null, 2)));
  }, []);
  return (
    <div>
      <h2>Audit Inspector</h2>
      <pre>{audit}</pre>
      <button onClick={() => {
        const blob = new Blob([audit], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'aifolio_audit.json';
        a.click();
      }}>Export Audit Report</button>
    </div>
  );
}
