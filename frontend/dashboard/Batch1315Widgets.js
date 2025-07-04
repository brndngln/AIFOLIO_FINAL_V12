// Batch1315Widgets.js
// SAFE AI Batches 13–15 React widgets. Each widget fetches and displays static, aggregate JSON data.
import React, { useEffect, useState } from 'react';
import {
  fetchOpenBankingRevenueReport,
  fetchMultiPartnerSyncSummary,
  fetchInnovationRadarReport,
  fetchPartnerEcosystemHealthCheck,
  fetchGlobalBusinessMap,
  fetchVaultCrossMarketFitReport,
  fetchPassivePartnershipMonitor,
  fetchAnnualBusinessHealthScorecard,
  fetchMultiChannelRevenueBreakdown,
  fetchContentLicensingStatusTracker,
  fetchAffiliateRevenueTracker,
  fetchReadinessCertification,
  fetchCrossNicheRevenueOverlapReport,
  fetchPartnerReputationScore,
  fetchAnnualVaultMarketFitIndex,
  fetchLegacyContentAgingTracker,
  fetchBusinessScalabilityIndex,
  fetchPlatformEcosystemStabilityReport,
  fetchLongTermComplianceRoadmap,
  fetchMultiYearBusinessPlanningSummary
} from './api';

function Widget({ title, fetchFn }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchFn().then(setData);
  }, [fetchFn]);
  return (
    <div style={{margin: '1.5em 0', padding: '1em', border: '1px solid #ddd', borderRadius: 8, background: '#fafbfc'}}>
      <h3 style={{marginBottom: '0.5em'}}>{title}</h3>
      <pre style={{fontSize: 13, background: '#f6f8fa', padding: 10, borderRadius: 6, overflowX: 'auto'}}>
        {data ? JSON.stringify(data, null, 2) : 'Loading...'}
      </pre>
    </div>
  );
}

// --- BATCH 13 ---
export const OpenBankingRevenueReport = () => (
  <Widget title="AI-Safe Open Banking Revenue Reports" fetchFn={fetchOpenBankingRevenueReport} />
);
export const MultiPartnerSyncSummary = () => (
  <Widget title="Multi-Partner SAFE AI Sync Summary" fetchFn={fetchMultiPartnerSyncSummary} />
);
export const InnovationRadarReport = () => (
  <Widget title="SAFE AI Innovation Radar Report" fetchFn={fetchInnovationRadarReport} />
);
export const PartnerEcosystemHealthCheck = () => (
  <Widget title="Partner Ecosystem Health Check" fetchFn={fetchPartnerEcosystemHealthCheck} />
);
export const GlobalBusinessMap = () => (
  <Widget title="AIFOLIO Global Business Map" fetchFn={fetchGlobalBusinessMap} />
);

// --- BATCH 14 ---
export const VaultCrossMarketFitReport = () => (
  <Widget title="Vault Cross-Market Fit Report" fetchFn={fetchVaultCrossMarketFitReport} />
);
export const PassivePartnershipMonitor = () => (
  <Widget title="SAFE AI Passive Partnership Monitor" fetchFn={fetchPassivePartnershipMonitor} />
);
export const AnnualBusinessHealthScorecard = () => (
  <Widget title="Annual SAFE AI Business Health Scorecard" fetchFn={fetchAnnualBusinessHealthScorecard} />
);
export const MultiChannelRevenueBreakdown = () => (
  <Widget title="Multi-Channel SAFE AI Revenue Breakdown" fetchFn={fetchMultiChannelRevenueBreakdown} />
);
export const ContentLicensingStatusTracker = () => (
  <Widget title="Content Licensing Status Tracker" fetchFn={fetchContentLicensingStatusTracker} />
);
export const AffiliateRevenueTracker = () => (
  <Widget title="Static Affiliate Revenue Tracker" fetchFn={fetchAffiliateRevenueTracker} />
);
export const ReadinessCertification = () => (
  <Widget title="Admin SAFE AI Readiness Certification" fetchFn={fetchReadinessCertification} />
);

// --- BATCH 15 ---
export const CrossNicheRevenueOverlapReport = () => (
  <Widget title="Cross-Niche Revenue Overlap Report" fetchFn={fetchCrossNicheRevenueOverlapReport} />
);
export const PartnerReputationScore = () => (
  <Widget title="SAFE AI Partner Reputation Score" fetchFn={fetchPartnerReputationScore} />
);
export const AnnualVaultMarketFitIndex = () => (
  <Widget title="Annual Vault Market Fit Index" fetchFn={fetchAnnualVaultMarketFitIndex} />
);
export const LegacyContentAgingTracker = () => (
  <Widget title="Legacy Content Aging Tracker" fetchFn={fetchLegacyContentAgingTracker} />
);
export const BusinessScalabilityIndex = () => (
  <Widget title="SAFE AI Business Scalability Index" fetchFn={fetchBusinessScalabilityIndex} />
);
export const PlatformEcosystemStabilityReport = () => (
  <Widget title="Platform Ecosystem Stability Report" fetchFn={fetchPlatformEcosystemStabilityReport} />
);
export const LongTermComplianceRoadmap = () => (
  <Widget title="SAFE AI Long-Term Compliance Roadmap" fetchFn={fetchLongTermComplianceRoadmap} />
);
export const MultiYearBusinessPlanningSummary = () => (
  <Widget title="SAFE AI Multi-Year Business Planning Summary" fetchFn={fetchMultiYearBusinessPlanningSummary} />
);
