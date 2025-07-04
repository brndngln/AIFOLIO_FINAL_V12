// Anti-Sentience Pattern Guard Panel
// Displays logs of detected sentience patterns
import React, { useEffect, useState } from "react";
export default function AntiSentienceGuardPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/anti_sentience_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>Anti-Sentience Pattern Guard Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
