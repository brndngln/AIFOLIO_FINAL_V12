// Auto-Recovery Panel
// Displays auto-recovery logs from backend
import React, { useEffect, useState } from "react";
export default function AutoRecoveryPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/auto_recovery_log")
      .then((res) => res.json())
      .then(setLogs);
  }, []);
  return (
    <div>
      <h2>Auto-Recovery Log</h2>
      <ul>
        {logs.map((line, i) => (
          <li key={i}>{line}</li>
        ))}
      </ul>
    </div>
  );
}
