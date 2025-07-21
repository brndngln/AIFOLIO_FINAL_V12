import React, { useState, useEffect } from "react";

export function SystemHealthBadge() {
  const [health, setHealth] = useState("loading");
  useEffect(() => {
    fetch("/batch-scaling/system-health")
      .then((r) => r.json())
      .then((data) => setHealth(data.status || "ok"));
  }, []);
  return (
    <div style={{ marginBottom: 16 }}>
      {health === "ok" && (
        <span
          style={{
            background: "#10b981",
            color: "#fff",
            padding: "4px 12px",
            borderRadius: 8,
            fontWeight: 600,
          }}
        >
          System Health: OK ✅
        </span>
      )}
      {health === "issues" && (
        <span
          style={{
            background: "#f59e0b",
            color: "#fff",
            padding: "4px 12px",
            borderRadius: 8,
            fontWeight: 600,
          }}
        >
          Issues Detected ⚠️
        </span>
      )}
      {health === "loading" && (
        <span
          style={{
            background: "#334155",
            color: "#fff",
            padding: "4px 12px",
            borderRadius: 8,
          }}
        >
          Checking system health…
        </span>
      )}
    </div>
  );
}

export function Batch17Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch17/${type}`);
      if (!res.ok) {
        setExportStatus(
          "Download failed — file not found. Please re-export or contact admin.",
        );
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get("Content-Disposition");
      const filename = contentDisp
        ? contentDisp.split("filename=")[1]
        : `batch17_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get("X-Last-Updated") || "");
    } catch {
      setExportStatus(
        "Download failed — file not found. Please re-export or contact admin.",
      );
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch17/pdf`).then((r) =>
      setLastUpdated(r.headers.get("X-Last-Updated") || ""),
    );
  }, []);
  return (
    <section className="batch17-widgets">
      <h2>Batch 17: SAFE AI Risk Mitigation</h2>
      <button onClick={() => exportBatch("pdf")}>Export PDF</button>
      <button onClick={() => exportBatch("csv")}>Export CSV</button>
      <span style={{ marginLeft: 12, color: "#64748b", fontSize: 13 }}>
        Last updated: {lastUpdated}
      </span>
      {exportStatus && <div className="export-status">{exportStatus}</div>}
    </section>
  );
}

export function Batch18Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch18/${type}`);
      if (!res.ok) {
        setExportStatus(
          "Download failed — file not found. Please re-export or contact admin.",
        );
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get("Content-Disposition");
      const filename = contentDisp
        ? contentDisp.split("filename=")[1]
        : `batch18_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get("X-Last-Updated") || "");
    } catch {
      setExportStatus(
        "Download failed — file not found. Please re-export or contact admin.",
      );
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch18/pdf`).then((r) =>
      setLastUpdated(r.headers.get("X-Last-Updated") || ""),
    );
  }, []);
  return (
    <section className="batch18-widgets">
      <h2>Batch 18: SAFE AI Partner Certification</h2>
      <button onClick={() => exportBatch("pdf")}>Export PDF</button>
      <button onClick={() => exportBatch("csv")}>Export CSV</button>
      <span style={{ marginLeft: 12, color: "#64748b", fontSize: 13 }}>
        Last updated: {lastUpdated}
      </span>
      {exportStatus && <div className="export-status">{exportStatus}</div>}
    </section>
  );
}

export function Batch19Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch19/${type}`);
      if (!res.ok) {
        setExportStatus(
          "Download failed — file not found. Please re-export or contact admin.",
        );
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get("Content-Disposition");
      const filename = contentDisp
        ? contentDisp.split("filename=")[1]
        : `batch19_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get("X-Last-Updated") || "");
    } catch {
      setExportStatus(
        "Download failed — file not found. Please re-export or contact admin.",
      );
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch19/pdf`).then((r) =>
      setLastUpdated(r.headers.get("X-Last-Updated") || ""),
    );
  }, []);
  return (
    <section className="batch19-widgets">
      <h2>Batch 19: SAFE AI Compliance Automation</h2>
      <button onClick={() => exportBatch("pdf")}>Export PDF</button>
      <button onClick={() => exportBatch("csv")}>Export CSV</button>
      <span style={{ marginLeft: 12, color: "#64748b", fontSize: 13 }}>
        Last updated: {lastUpdated}
      </span>
      {exportStatus && <div className="export-status">{exportStatus}</div>}
    </section>
  );
}

export function Batch20Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch20/${type}`);
      if (!res.ok) {
        setExportStatus(
          "Download failed — file not found. Please re-export or contact admin.",
        );
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get("Content-Disposition");
      const filename = contentDisp
        ? contentDisp.split("filename=")[1]
        : `batch20_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get("X-Last-Updated") || "");
    } catch {
      setExportStatus(
        "Download failed — file not found. Please re-export or contact admin.",
      );
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch20/pdf`).then((r) =>
      setLastUpdated(r.headers.get("X-Last-Updated") || ""),
    );
  }, []);
  return (
    <section className="batch20-widgets">
      <h2>Batch 20: SAFE AI Public Reporting</h2>
      <button onClick={() => exportBatch("pdf")}>Export PDF</button>
      <button onClick={() => exportBatch("csv")}>Export CSV</button>
      <span style={{ marginLeft: 12, color: "#64748b", fontSize: 13 }}>
        Last updated: {lastUpdated}
      </span>
      {exportStatus && <div className="export-status">{exportStatus}</div>}
    </section>
  );
}

export function Batch16Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch16/${type}`);
      if (!res.ok) {
        setExportStatus(
          "Download failed — file not found. Please re-export or contact admin.",
        );
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get("Content-Disposition");
      const filename = contentDisp
        ? contentDisp.split("filename=")[1]
        : `batch16_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get("X-Last-Updated") || "");
    } catch {
      setExportStatus(
        "Download failed — file not found. Please re-export or contact admin.",
      );
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch16/pdf`).then((r) =>
      setLastUpdated(r.headers.get("X-Last-Updated") || ""),
    );
  }, []);
  return (
    <section className="batch16-widgets">
      <h2>Batch 16: Global Business Consolidation</h2>
      <ul>
        <li>Multi-Currency SAFE AI Revenue Tracking (static)</li>
        <li>AI-Safe Tax Region Reporting</li>
        <li>Static Vault Licensing Map</li>
        <li>Multi-Region Compliance Status Tracker</li>
        <li>Partner API Legal Health Map</li>
        <li>Global Vault Ecosystem Maturity Scorecard</li>
      </ul>
      <div className="static-widget">
        <button onClick={() => exportBatch("pdf")}>Export Batch 16 PDF</button>
        <button onClick={() => exportBatch("csv")}>Export Batch 16 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
  );
}

import PartnerCertificationForm from "./PartnerCertificationForm";

export function PartnerCertificationWidgets() {
  const [exportStatus, setExportStatus] = useState("");
  function handleExport(type, partner) {
    window.open(
      `/batch-scaling/partner-certifications/export?type=${type}&partner=${encodeURIComponent(partner)}`,
      "_blank",
    );
    setExportStatus(
      `Partner Certification ${type.toUpperCase()} export started!`,
    );
    setTimeout(() => setExportStatus(""), 3000);
  }
  function exportPublicReport() {
    window.open(`/batch-scaling/public-report/export`, "_blank");
    setExportStatus("Public SAFE AI Report PDF export started!");
    setTimeout(() => setExportStatus(""), 3000);
  }
  return (
    <section className="partner-certification-widgets">
      <h2>SAFE AI Partner Certification System</h2>
      <ul>
        <li>SAFE AI Partner Certification Tracker</li>
        <li>Partner Self-Certification Submission UI</li>
        <li>Partner Certification Audit Report Generator</li>
        <li>Annual Partner Certification Export</li>
      </ul>
      <PartnerCertificationForm onExport={handleExport} />
      <div className="static-widget">
        <button onClick={exportPublicReport}>
          Export Public SAFE AI Report (PDF)
        </button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
      <div className="static-widget">
        (Admin-reviewed, static forms/exports only)
      </div>
    </section>
  );
}
