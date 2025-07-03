import React, { useEffect, useState } from "react";

export default function Phase9AuditLogWidget({ logPath = "/distribution/legal_exports/phase9_empire_audit_log.txt" }) {
  const [log, setLog] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(logPath)
      .then(res => {
        if (!res.ok) throw new Error("Could not fetch audit log");
        return res.text();
      })
      .then(setLog)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [logPath]);

  return (
    <div style={{border: '1px solid #bbb', borderRadius: 6, padding: 12, background: '#fafcff', marginBottom: 20}}>
      <h3 style={{fontSize: '1.1em', margin: 0, marginBottom: 8}}>Phase 9+ Audit Log</h3>
      {loading && <div>Loading...</div>}
      {error && <div style={{color: 'red'}}>Error: {error}</div>}
      {!loading && !error && (
        <pre style={{fontSize: 13, maxHeight: 200, overflowY: 'auto', background: '#f7f7fa', padding: 8, borderRadius: 4}}>{log || "No log entries yet."}</pre>
      )}
    </div>
  );
}
