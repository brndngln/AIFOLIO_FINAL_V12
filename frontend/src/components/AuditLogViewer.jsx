import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AuditLogViewer({ token }) {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios.get("/api/ai-safety-log", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => setLogs(res.data))
      .catch(() => setLogs([]))
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="audit-log-viewer">
      <h3>SAFE AI Audit Log</h3>
      {loading ? <div>Loading logs...</div> : (
        <ul>
          {logs.map((entry, i) => (
            <li key={i}>
              <pre>{JSON.stringify(entry, null, 2)}</pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
