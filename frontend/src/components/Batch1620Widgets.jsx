import React from "react";

import React, { useState, useEffect } from "react";

export function SystemHealthBadge() {
  const [health, setHealth] = useState('loading');
  useEffect(() => {
    fetch('/batch-scaling/system-health')
      .then(r => r.json())
      .then(data => setHealth(data.status || 'ok'));
  }, []);
  return (
    <div style={{marginBottom:16}}>
      {health === 'ok' && (
        <span style={{background:'#10b981',color:'#fff',padding:'4px 12px',borderRadius:8,fontWeight:600}}>System Health: OK ✅</span>
      )}
      {health === 'issues' && (
        <span style={{background:'#f59e0b',color:'#fff',padding:'4px 12px',borderRadius:8,fontWeight:600}}>Issues Detected ⚠️</span>
      )}
      {health === 'loading' && (
        <span style={{background:'#334155',color:'#fff',padding:'4px 12px',borderRadius:8}}>Checking system health…</span>
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
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch17_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch17/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
  }, []);
  return (
    <section className="batch17-widgets">
      <h2>Batch 17: SAFE AI Risk Mitigation</h2>
      <button onClick={() => exportBatch('pdf')}>Export PDF</button>
      <button onClick={() => exportBatch('csv')}>Export CSV</button>
      <span style={{marginLeft:12, color:'#64748b', fontSize:13}}>Last updated: {lastUpdated}</span>
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
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch18_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch18/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
  }, []);
  return (
    <section className="batch18-widgets">
      <h2>Batch 18: SAFE AI Partner Certification</h2>
      <button onClick={() => exportBatch('pdf')}>Export PDF</button>
      <button onClick={() => exportBatch('csv')}>Export CSV</button>
      <span style={{marginLeft:12, color:'#64748b', fontSize:13}}>Last updated: {lastUpdated}</span>
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
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch19_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch19/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
  }, []);
  return (
    <section className="batch19-widgets">
      <h2>Batch 19: SAFE AI Compliance Automation</h2>
      <button onClick={() => exportBatch('pdf')}>Export PDF</button>
      <button onClick={() => exportBatch('csv')}>Export CSV</button>
      <span style={{marginLeft:12, color:'#64748b', fontSize:13}}>Last updated: {lastUpdated}</span>
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
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch20_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch20/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
  }, []);
  return (
    <section className="batch20-widgets">
      <h2>Batch 20: SAFE AI Public Reporting</h2>
      <button onClick={() => exportBatch('pdf')}>Export PDF</button>
      <button onClick={() => exportBatch('csv')}>Export CSV</button>
      <span style={{marginLeft:12, color:'#64748b', fontSize:13}}>Last updated: {lastUpdated}</span>
      {exportStatus && <div className="export-status">{exportStatus}</div>}
    </section>
  );
}

// Partner Certification and Public Report widgets should be similarly updated for SAFE AI UX.
  const [exportStatus, setExportStatus] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");
  async function exportBatch(type) {
    setExportStatus("");
    try {
      const res = await fetch(`/batch-scaling/batch-export/batch16/${type}`);
      if (!res.ok) {
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch16_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    // Fetch last updated on mount
    fetch(`/batch-scaling/batch-export/batch16/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
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
        <button onClick={() => exportBatch('pdf')}>Export Batch 16 PDF</button>
        <button onClick={() => exportBatch('csv')}>Export Batch 16 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
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
        setExportStatus("Download failed — file not found. Please re-export or contact admin.");
        return;
      }
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp ? contentDisp.split('filename=')[1] : `batch17_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setExportStatus("Export complete — download ready.");
      setTimeout(() => setExportStatus(""), 3000);
      setLastUpdated(res.headers.get('X-Last-Updated') || "");
    } catch {
      setExportStatus("Download failed — file not found. Please re-export or contact admin.");
    }
  }
  useEffect(() => {
    fetch(`/batch-scaling/batch-export/batch17/pdf`).then(r => setLastUpdated(r.headers.get('X-Last-Updated') || ""));
  }, []);
  return (
    <section className="batch17-widgets">
      <h2>Batch 17: Executive SAFE AI Intelligence</h2>
      <ul>
        <li>Annual SAFE AI Executive Summary Report</li>
        <li>SAFE AI CEO Dashboard (static only)</li>
        <li>Global SAFE AI Business Impact Map</li>
        <li>Partner Legal Term Tracker</li>
        <li>AI-Safe ESG Score Report</li>
        <li>Cross-Vault IP Overlap Map</li>
      </ul>
      <div className="static-widget">
        <button onClick={() => exportBatch('pdf')}>Export Batch 17 PDF</button>
        <button onClick={() => exportBatch('csv')}>Export Batch 17 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
  );
}

export function Batch18Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch18/${type}`, '_blank');
    setExportStatus(`Batch 18 ${type.toUpperCase()} export started!`);
    setTimeout(() => setExportStatus(""), 3000);
  }
  return (
    <section className="batch18-widgets">
      <h2>Batch 18: SAFE AI Strategic Governance</h2>
      <ul>
        <li>Long-Term SAFE AI System Resilience Audit</li>
        <li>Cross-Partner SAFE AI Alignment Report</li>
        <li>SAFE AI Governance Board Report Generator</li>
        <li>SAFE AI Multi-Year Compliance Tracker</li>
        <li>External Auditor SAFE AI Certification Export</li>
        <li>SAFE AI Roadmap Summary Export</li>
        <li>Partner Certification System (see below)</li>
      </ul>
      <div className="static-widget">
        <button onClick={() => exportBatch('pdf')}>Export Batch 18 PDF</button>
        <button onClick={() => exportBatch('csv')}>Export Batch 18 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
  );
}

export function Batch19Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch19/${type}`, '_blank');
    setExportStatus(`Batch 19 ${type.toUpperCase()} export started!`);
    setTimeout(() => setExportStatus(""), 3000);
  }
  return (
    <section className="batch19-widgets">
      <h2>Batch 19: Global + Web3 SAFE AI Scaling</h2>
      <ul>
        <li>Web3 SAFE AI Legal Compatibility Map</li>
        <li>SAFE AI Cross-Chain Revenue Tracker (static)</li>
        <li>Static NFT Licensing Tracker</li>
        <li>Web3 Partner Ecosystem Audit Report</li>
        <li>SAFE AI Blockchain Transparency Export</li>
        <li>SAFE AI Digital Asset IP Risk Report</li>
      </ul>
      <div className="static-widget">
        <button onClick={() => exportBatch('pdf')}>Export Batch 19 PDF</button>
        <button onClick={() => exportBatch('csv')}>Export Batch 19 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
  );
}

export function Batch20Widgets() {
  const [exportStatus, setExportStatus] = useState("");
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch20/${type}`, '_blank');
    setExportStatus(`Batch 20 ${type.toUpperCase()} export started!`);
    setTimeout(() => setExportStatus(""), 3000);
  }
  return (
    <section className="batch20-widgets">
      <h2>Batch 20: Enterprise SAFE AI Future-Ready</h2>
      <ul>
        <li>SAFE AI Enterprise Business Maturity Index</li>
        <li>SAFE AI Future Trends Manual Input Tracker</li>
        <li>AI-Policy Cross-Check Generator</li>
        <li>Global SAFE AI Partner Network Health Report</li>
        <li>SAFE AI System Renewal Planner</li>
        <li>SAFE AI “Trusted Partner” Public Report Generator</li>
      </ul>
      <div className="static-widget">
        <button onClick={() => exportBatch('pdf')}>Export Batch 20 PDF</button>
        <button onClick={() => exportBatch('csv')}>Export Batch 20 CSV</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
    </section>
  );
}

import PartnerCertificationForm from "./PartnerCertificationForm";

export function PartnerCertificationWidgets() {
  const [exportStatus, setExportStatus] = useState("");
  function handleExport(type, partner) {
    window.open(`/batch-scaling/partner-certifications/export?type=${type}&partner=${encodeURIComponent(partner)}`, '_blank');
    setExportStatus(`Partner Certification ${type.toUpperCase()} export started!`);
    setTimeout(() => setExportStatus(""), 3000);
  }
  function exportPublicReport() {
    window.open(`/batch-scaling/public-report/export`, '_blank');
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
        <button onClick={exportPublicReport}>Export Public SAFE AI Report (PDF)</button>
        {exportStatus && <div className="export-status">{exportStatus}</div>}
      </div>
      <div className="static-widget">(Admin-reviewed, static forms/exports only)</div>
    </section>
  );
}
