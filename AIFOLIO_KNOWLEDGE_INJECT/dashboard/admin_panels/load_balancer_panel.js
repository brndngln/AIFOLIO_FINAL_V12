// Load Balancer Panel
// Displays load balancer logs from backend
import React, { useEffect, useState } from "react";
export default function LoadBalancerPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/load_balancer_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>Load Balancer Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
