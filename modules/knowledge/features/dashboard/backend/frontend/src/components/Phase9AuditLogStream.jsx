import React, { useEffect, useRef, useState } from "react";

export default function Phase9AuditLogStream({
  apiBase = "http://localhost:8090",
}) {
  const [lines, setLines] = useState([]);
  const [connected, setConnected] = useState(false);
  const eventSourceRef = useRef(null);

  useEffect(() => {
    const es = new EventSource(`${apiBase}/phase9/audit_log/stream`);
    eventSourceRef.current = es;
    setConnected(true);
    es.onmessage = (e) => {
      setLines((lines) => [...lines.slice(-199), e.data]);
    };
    es.onerror = () => {
      setConnected(false);
      es.close();
    };
    return () => es.close();
  }, [apiBase]);

  return (
    <div
      style={{
        border: "1px solid #b7e",
        borderRadius: 6,
        padding: 10,
        marginBottom: 18,
        background: "#f8f5ff",
      }}
    >
      <b>Phase 9+ Real-Time Audit Log Stream</b>
      <span style={{ marginLeft: 12, color: connected ? "#27b36a" : "#d67" }}>
        {connected ? "Connected" : "Disconnected"}
      </span>
      <pre
        style={{
          fontSize: 12,
          maxHeight: 180,
          overflowY: "auto",
          margin: 0,
          background: "none",
          padding: 0,
        }}
      >
        {lines.join("\n")}
      </pre>
    </div>
  );
}
