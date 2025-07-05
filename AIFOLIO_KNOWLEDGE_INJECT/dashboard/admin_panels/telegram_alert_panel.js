// Telegram Alert Panel
// Displays Telegram alert logs from backend (stub)
import React, { useEffect, useState } from "react";
export default function TelegramAlertPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/telegram_alert_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>Telegram Alert Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
