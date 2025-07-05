// AIFOLIO SAFE AI Batch 5–6 Widgets
// Provides UI components for new analytics endpoints in Batches 5–6
import React, { useEffect, useState } from 'react';
import {
  fetchMultiVaultLaunchPlan,
  fetchCompetitorComparison,
  fetchAnnualRevenueTrend,
  fetchVaultLifecycleStage,
  fetchSeasonalSalesPattern,
  fetchSystemLoadReport,
  fetchStaticFeatureUsageReport,
  fetchLegalDocumentExpiryTracker,
  fetchPolicyUpdateNotifier,
  fetchPlatformHealthRedFlags
} from './api';

export function MultiVaultLaunchPlanner() {
  const [data, setData] = useState({});
  useEffect(() => { fetchMultiVaultLaunchPlan().then(setData); }, []);
  return <section><h2>Multi-Vault Launch Planner</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function CompetitorComparison() {
  const [data, setData] = useState({});
  useEffect(() => { fetchCompetitorComparison().then(setData); }, []);
  return <section><h2>Static Competitor Comparison</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function AnnualRevenueTrend() {
  const [data, setData] = useState({});
  useEffect(() => { fetchAnnualRevenueTrend().then(setData); }, []);
  return <section><h2>Annual Revenue Trend Report</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function VaultLifecycleStageTracker() {
  const [data, setData] = useState({});
  useEffect(() => { fetchVaultLifecycleStage().then(setData); }, []);
  return <section><h2>Vault Lifecycle Stage Tracker</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function SeasonalSalesPatternReport() {
  const [data, setData] = useState({});
  useEffect(() => { fetchSeasonalSalesPattern().then(setData); }, []);
  return <section><h2>Seasonal Sales Pattern Report</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function SystemLoadReport() {
  const [data, setData] = useState({});
  useEffect(() => { fetchSystemLoadReport().then(setData); }, []);
  return <section><h2>System Load / Traffic Report</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function StaticFeatureUsageReport() {
  const [data, setData] = useState({});
  useEffect(() => { fetchStaticFeatureUsageReport().then(setData); }, []);
  return <section><h2>Feature Usage Report</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function LegalDocumentExpiryTracker() {
  const [data, setData] = useState({});
  useEffect(() => { fetchLegalDocumentExpiryTracker().then(setData); }, []);
  return <section><h2>Legal Document Expiry Tracker</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function PolicyUpdateNotifier() {
  const [data, setData] = useState({});
  useEffect(() => { fetchPolicyUpdateNotifier().then(setData); }, []);
  return <section><h2>Policy Update Notifier</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}

export function PlatformHealthRedFlags() {
  const [data, setData] = useState({});
  useEffect(() => { fetchPlatformHealthRedFlags().then(setData); }, []);
  return <section><h2>Platform Health Red Flags</h2><pre>{JSON.stringify(data, null, 2)}</pre></section>;
}
