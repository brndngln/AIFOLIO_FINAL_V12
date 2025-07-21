// Style/Voice Tuner Panel
// Displays style-tuned outputs for admin review
import React, { useEffect, useState } from "react";
export default function StyleVoiceTunerPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/style_tuner_log")
      .then((res) => res.json())
      .then(setLogs);
  }, []);
  return (
    <div>
      <h2>Style/Voice Tuner Log</h2>
      <ul>
        {logs.map((line, i) => (
          <li key={i}>{line}</li>
        ))}
      </ul>
    </div>
  );
}
