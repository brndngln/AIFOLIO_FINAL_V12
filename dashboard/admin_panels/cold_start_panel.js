// Cold Start Minimizer Panel
// Displays cold start logs from backend
import React, { useEffect, useState } from "react";
export default function ColdStartPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/cold_start_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>Cold Start Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
