import React, { useState } from "react";

export default function ExportPanel() {
  const [format, setFormat] = useState("pdf");
  const [watermark, setWatermark] = useState(false);
  const [signature, setSignature] = useState(false);
  const [status, setStatus] = useState("");

  const handleExport = async () => {
    setStatus("Exporting...");
    try {
      const res = await fetch("/api/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format, watermark, signature }),
      });
      if (!res.ok) throw new Error("Export failed");
      const data = await res.json();
      setStatus(
        data.message ||
          `Exported as ${format.toUpperCase()}${watermark ? " with watermark" : ""}${signature ? " with signature" : ""}`,
      );
    } catch (err) {
      setStatus("Export failed: " + (err.message || err));
    }
  };

  return (
    <div
      className="export-panel"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
      }}
    >
      <h2>Elite Export Panel</h2>
      <div style={{ marginBottom: 16 }}>
        <label>Format: </label>
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          <option value="pdf">PDF</option>
          <option value="docx">DOCX</option>
          <option value="xlsx">XLSX</option>
          <option value="html">HTML</option>
        </select>
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>
          <input
            type="checkbox"
            checked={watermark}
            onChange={(e) => setWatermark(e.target.checked)}
          />{" "}
          Branded Watermark
        </label>
        <label style={{ marginLeft: 16 }}>
          <input
            type="checkbox"
            checked={signature}
            onChange={(e) => setSignature(e.target.checked)}
          />{" "}
          Digital Signature
        </label>
      </div>
      <button
        onClick={handleExport}
        style={{
          background: "#00e6ff",
          color: "#181e2b",
          border: "none",
          borderRadius: 8,
          padding: "8px 16px",
          fontWeight: "bold",
        }}
      >
        Export
      </button>
      {status && (
        <div style={{ marginTop: 16, color: "#00e6ff" }}>{status}</div>
      )}
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          All exports are SAFE AI-compliant, owner-branded, and licensing-ready.
          Advanced options for elite business needs.
        </em>
      </div>
    </div>
  );
}
