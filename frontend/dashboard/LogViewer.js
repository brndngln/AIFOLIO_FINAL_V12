// AIFOLIO SAFE AI Log Viewer Component
// Allows admin to view/export analytics, pipeline, and compliance logs
import React, { useEffect, useState } from 'react';
import { fetchAdminLogs } from './api';

export default function LogViewer() {
  const [logs, setLogs] = useState('');
  useEffect(() => {
    fetchAdminLogs().then(data => setLogs(JSON.stringify(data, null, 2)));
  }, []);
  return (
    <div>
      <h2>Analytics & Pipeline Logs</h2>
      <pre>{logs}</pre>
      <button onClick={() => {
        const blob = new Blob([logs], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'aifolio_logs.json';
        a.click();
      }}>Export Logs</button>
    </div>
  );
}
