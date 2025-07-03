// Webhook Latency Monitor Panel
// Displays webhook latency logs from backend
import React, { useEffect, useState } from "react";
export default function WebhookLatencyPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/webhook_latency_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>Webhook Latency Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
