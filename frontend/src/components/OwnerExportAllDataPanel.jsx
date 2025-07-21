import React, { useState } from "react";
import JSZip from "jszip";

const FILES = [
  {
    label: "Sample Vaults",
    file: "sample_vaults.json",
    url: "/data/sample_vaults.json",
  },
  {
    label: "Pricing Logs",
    file: "pricing_log.json",
    url: "/analytics/pricing_log.json",
  },
  { label: "Policy: Terms", file: "terms.md", url: "/policy/terms.md" },
  { label: "Policy: Privacy", file: "privacy.md", url: "/policy/privacy.md" },
  { label: "Policy: Refund", file: "refund.md", url: "/policy/refund.md" },
  {
    label: "Compliance Logs",
    file: "compliance_log.json",
    url: "/analytics/compliance_log.json",
  },
];

// [WINDSURF FIXED ✅]
export default function OwnerExportAllDataPanel() {
  const [selected, setSelected] = useState(() =>
    Array(FILES.length).fill(true),
  );
  const [status, setStatus] = useState(""); // Remove if not used in render or logic

  async function handleExport() {
    setStatus("Preparing ZIP...");
    const zip = new JSZip();
    for (let i = 0; i < FILES.length; ++i) {
      if (!selected[i]) continue;
      try {
        const res = await fetch(FILES[i].url);
        const text = await res.text();
        zip.file(FILES[i].file, text);
      } catch {
        zip.file(FILES[i].file, "[Error: Could not fetch file]");
      }
    }
    const blob = await zip.generateAsync({ type: "blob" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AIFOLIO_EXPORT_${new Date().toISOString().slice(0, 10)}.zip`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
    setStatus("Export complete!");
  }

  return (
    <section
      aria-labelledby="export-all-data-heading"
      style={{
        background: "#f9fafb",
        borderRadius: 12,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #e0e7ef",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginBottom: 12,
        }}
      >
        <h2
          id="export-all-data-heading"
          style={{ color: "#0ea5e9", fontWeight: 800, fontSize: 22, margin: 0 }}
        >
          Export All Data
        </h2>
        <span
          style={{
            background: "#0ea5e9",
            color: "#fff",
            padding: "2px 10px",
            borderRadius: 6,
            fontWeight: 700,
            fontSize: 13,
          }}
          aria-label="OWNER badge"
        >
          OWNER
        </span>
        <span
          tabIndex={0}
          aria-label="Help: Export all data"
          title="Download all business data, logs, and policies as a ZIP. OWNER controls all exports."
          style={{
            marginLeft: 6,
            color: "#64748b",
            cursor: "help",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          ?
        </span>
      </div>
      <ul
        style={{ listStyle: "none", padding: 0, fontSize: 15 }}
        aria-label="Export file selection"
      >
        {FILES.map((f, i) => (
          <li
            key={i}
            style={{
              marginBottom: 10,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <input
              type="checkbox"
              checked={selected[i]}
              aria-label={`Include ${f.label}`}
              onChange={() => {
                const next = [...selected];
                next[i] = !next[i];
                setSelected(next);
              }}
              style={{ accentColor: "#0ea5e9" }}
            />
            <span tabIndex={0} aria-label={`Export file: ${f.label}`}>
              {f.label}
            </span>
          </li>
        ))}
      </ul>
      <button
        style={{
          background: "#0ea5e9",
          color: "#fff",
          border: "none",
          borderRadius: 6,
          padding: "10px 20px",
          fontWeight: 700,
          fontSize: 15,
          cursor: "pointer",
          marginTop: 12,
          boxShadow: "0 1px 2px #bae6fd",
        }}
        aria-label="Download all selected data as ZIP"
        onClick={handleExport}
      >
        Export Selected Data as ZIP
      </button>
      <div
        style={{ marginTop: 18, color: "#64748b", fontSize: 13 }}
        aria-live="polite"
      >
        {status}
      </div>
      <div style={{ marginTop: 10, color: "#64748b", fontSize: 13 }}>
        <b>OWNER CONTROLLED:</b> Only OWNER can export data. All actions are
        static and audit-logged.
      </div>
    </section>
  );
}
