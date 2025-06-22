import React from "react";

export function Batch16Widgets() {
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch16/${type}`, '_blank');
  }
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
      </div>
    </section>
  );
}

export function Batch17Widgets() {
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch17/${type}`, '_blank');
  }
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
      </div>
    </section>
  );
}

export function Batch18Widgets() {
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch18/${type}`, '_blank');
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
      </div>
    </section>
  );
}

export function Batch19Widgets() {
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch19/${type}`, '_blank');
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
      </div>
    </section>
  );
}

export function Batch20Widgets() {
  function exportBatch(type) {
    window.open(`/batch-scaling/batch-export/batch20/${type}`, '_blank');
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
      </div>
    </section>
  );
}

import PartnerCertificationForm from "./PartnerCertificationForm";

export function PartnerCertificationWidgets() {
  function handleExport(type, partner) {
    window.open(`/batch-scaling/partner-certifications/export?type=${type}&partner=${encodeURIComponent(partner)}`, '_blank');
  }
  function exportPublicReport() {
    window.open(`/batch-scaling/public-report/export`, '_blank');
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
      </div>
      <div className="static-widget">(Admin-reviewed, static forms/exports only)</div>
    </section>
  );
}
