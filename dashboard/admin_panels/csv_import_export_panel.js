// CSV Bulk Import/Export Panel
// Displays CSV import/export logs from backend
import React, { useEffect, useState } from "react";
export default function CsvImportExportPanel() {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    fetch("/api/csv_import_export_log").then(res => res.json()).then(setLogs);
  }, []);
  return (
    <div>
      <h2>CSV Import/Export Log</h2>
      <ul>
        {logs.map((line, i) => <li key={i}>{line}</li>)}
      </ul>
    </div>
  );
}
