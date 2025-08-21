import React, { useEffect, useState } from "react";

function AuditLogViewer({ token }) {
  const [log, setLog] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/audit_log", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.text())
      .then((data) => {
        setLog(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load audit log");
        setLoading(false);
      });
  }, [token]);

  return (
    <div
      style={{
        background: "#fff",
        padding: 24,
        borderRadius: 8,
        marginTop: 32,
      }}
    >
      <h2>Audit Log</h2>
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div>{error}</div>
      ) : (
        <pre style={{ maxHeight: 400, overflowY: "auto" }}>{log}</pre>
      )}
    </div>
  );
}

export default AuditLogViewer;
