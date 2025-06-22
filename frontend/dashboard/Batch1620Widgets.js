// AIFOLIO SAFE AI Batches 16–20 + Partner Certification Widgets
// Each widget fetches static, deterministic SAFE AI data via frontend/api.js
import React, { useEffect, useState } from 'react';
import * as api from './api';

function Widget({ title, fetchFn }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  useEffect(() => {
    fetchFn()
      .then(setData)
      .catch(e => setError(e.message || 'Error loading data'));
  }, [fetchFn]);
  return (
    <div className="safe-widget">
      <h4>{title}</h4>
      {error && <div className="error">{error}</div>}
      <pre style={{ fontSize: 12, background: '#f8f8f8', padding: 8, borderRadius: 4, overflowX: 'auto' }}>{data ? JSON.stringify(data, null, 2) : 'Loading...'}</pre>
    </div>
  );
}

export function Batch16Widgets() {
  return <section><h3>Batch 16: Global Business Consolidation</h3>
    <Widget title="Multi-Currency SAFE AI Revenue Tracking" fetchFn={api.fetchMultiCurrencyRevenueTracking} />
    <Widget title="AI-Safe Tax Region Reporting" fetchFn={api.fetchTaxRegionReport} />
    <Widget title="Static Vault Licensing Map (global)" fetchFn={api.fetchVaultLicensingMap} />
    <Widget title="Multi-Region Compliance Status Tracker" fetchFn={api.fetchMultiRegionComplianceStatus} />
    <Widget title="Partner API Legal Health Map" fetchFn={api.fetchPartnerAPILegalHealthMap} />
    <Widget title="Global Vault Ecosystem Maturity Scorecard" fetchFn={api.fetchGlobalVaultEcosystemMaturityScorecard} />
  </section>;
}

export function Batch17Widgets() {
  return <section><h3>Batch 17: Executive SAFE AI Intelligence</h3>
    <Widget title="Annual SAFE AI Executive Summary Report" fetchFn={api.fetchAnnualExecutiveSummaryReport} />
    <Widget title="SAFE AI CEO Dashboard" fetchFn={api.fetchCEODashboard} />
    <Widget title="Global SAFE AI Business Impact Map" fetchFn={api.fetchBusinessImpactMap} />
    <Widget title="Partner Legal Term Tracker" fetchFn={api.fetchPartnerLegalTermTracker} />
    <Widget title="AI-Safe ESG Score Report" fetchFn={api.fetchESGScoreReport} />
    <Widget title="Cross-Vault IP Overlap Map" fetchFn={api.fetchCrossVaultIPOverlapMap} />
  </section>;
}

export function Batch18Widgets() {
  return <section><h3>Batch 18: SAFE AI Strategic Governance</h3>
    <Widget title="Long-Term SAFE AI System Resilience Audit" fetchFn={api.fetchLongTermSystemResilienceAudit} />
    <Widget title="Cross-Partner SAFE AI Alignment Report" fetchFn={api.fetchCrossPartnerAlignmentReport} />
    <Widget title="SAFE AI Governance Board Report Generator" fetchFn={api.fetchGovernanceBoardReport} />
    <Widget title="SAFE AI Multi-Year Compliance Tracker" fetchFn={api.fetchMultiYearComplianceTracker} />
    <Widget title="External Auditor SAFE AI Certification Export" fetchFn={api.fetchExternalAuditorCertificationExport} />
    <Widget title="SAFE AI Roadmap Summary Export" fetchFn={api.fetchRoadmapSummaryExport} />
  </section>;
}

export function PartnerCertificationWidgets() {
  return <section><h3>Partner Certification System</h3>
    <Widget title="SAFE AI Partner Certification Tracker" fetchFn={api.fetchPartnerCertificationTracker} />
    <Widget title="Partner Self-Certification Submission UI" fetchFn={api.fetchPartnerSelfCertificationSubmission} />
  </section>;
}

// Admin Audit Log Widget (for admin users)
export function AdminAuditLogWidget({limit=20,action,pattern}) {
  const [log, setLog] = useState([]);
  const [error, setError] = useState(null);
  useEffect(() => {
    api.fetchAISafetyAuditLog({limit,action,pattern})
      .then(res => setLog(res.audit_log || []))
      .catch(e => setError(e.message || 'Error loading audit log'));
  }, [limit,action,pattern]);
  return (
    <section>
      <h3>SAFE AI Audit Log</h3>
      {error && <div className="error">{error}</div>}
      <pre style={{ fontSize: 12, background: '#f8f8f8', padding: 8, borderRadius: 4, overflowX: 'auto', maxHeight: 320 }}>{log.length ? JSON.stringify(log, null, 2) : 'No recent audit log entries.'}</pre>
    </section>
  );
}
