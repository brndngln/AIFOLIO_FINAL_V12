// Synthetic Monitoring Panel
// Displays synthetic monitoring results from backend
import React, { useEffect, useState } from "react";
export default function SyntheticMonitoringPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/synthetic_monitor_log")
      .then((res) => res.json())
      .then(setLogs);
  }, []);
  return (
    <div>
      <h2>Synthetic Monitoring Log</h2>
      <ul>
        {logs.map((line, i) => (
          <li key={i}>{line}</li>
        ))}
      </ul>
    </div>
  );
}
