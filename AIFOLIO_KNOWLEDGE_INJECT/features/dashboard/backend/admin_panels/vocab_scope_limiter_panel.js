// Vocabulary Scope Limiter Panel
// Displays outputs restricted by vocabulary scope limiter
import React, { useEffect, useState } from "react";
export default function VocabScopeLimiterPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/vocab_limiter_log")
      .then((res) => res.json())
      .then(setLogs);
  }, []);
  return (
    <div>
      <h2>Vocabulary Scope Limiter Log</h2>
      <ul>
        {logs.map((line, i) => (
          <li key={i}>{line}</li>
        ))}
      </ul>
    </div>
  );
}
