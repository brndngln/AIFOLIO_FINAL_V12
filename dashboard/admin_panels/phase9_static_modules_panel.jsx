// Phase 9+ SAFE AI Empire Modules Panel
import React from "react";

import { useState } from "react";

const MODULE_API_MAP = [
  // [Display Name, Endpoint, Method, Example Payload (if POST, else null)]
  ["AI static Competitive Moat Builder", "/phase9/competitive_moat", "POST", {vault_data: {}}],
  ["AI static Global Trend Forecaster", "/phase9/global_trend_forecast", "GET", null],
  ["AI static Market Saturation Scanner", "/phase9/market_saturation_scan", "POST", {market: ""}],
  ["AI static Niche Rejuvenation Planner", "/phase9/niche_rejuvenation_plan", "POST", {niche: ""}],
  ["AI static Opportunity Scoring Engine", "/phase9/opportunity_score", "POST", {opportunity: {}}],
  ["AI static Brand Resilience Evaluator", "/phase9/brand_resilience_evaluate", "POST", {brand: ""}],
  ["AI static Seasonal Trend Profiler", "/phase9/seasonal_trend_profile", "POST", {season: ""}],
  // Defensive & Legal Advance Monitors
  ["AI static Legal Threat Horizon Scanner", "/phase9/legal_threat_horizon_scan", "GET", null],
  ["AI static Compliance Landscape Visualizer", "/phase9/compliance_landscape_visualize", "GET", null],
  ["AI static Emerging IP Law Tracker", "/phase9/emerging_ip_law_track", "GET", null],
  ["AI static Regulatory Pressure Predictor", "/phase9/regulatory_pressure_predict", "GET", null],
  ["AI static Competitor Legal Shift Detector", "/phase9/competitor_legal_shift_detect", "GET", null],
  ["AI static Emerging Litigation Risk Map", "/phase9/emerging_litigation_risk_map", "GET", null],
  ["AI static GDPR/CCPA/EU AI Act Early Warning Monitor", "/phase9/gdpr_ccpa_eu_ai_act_monitor", "GET", null],
  // Market Positioning Optimizers
  ["AI static Vault Network Effects Mapper", "/phase9/vault_network_effects_map", "POST", {vaults: []}],
  ["AI static Optimal Bundle Timing Predictor", "/phase9/optimal_bundle_timing_predict", "GET", null],
  ["AI static Cross-Market Brand Map", "/phase9/cross_market_brand_map", "POST", {brands: []}],
  ["AI static 'Empire Strength' KPI dashboards", "/phase9/empire_strength_kpi_dashboard", "GET", null],
  ["AI static Price Competitiveness Map", "/phase9/price_competitiveness_map", "POST", {prices: []}],
  ["AI static Strategic Partnership Opportunity Detector", "/phase9/strategic_partnership_opportunity_detect", "GET", null],
  // AI-on-AI Resilience & Oversight
  ["Full SAFE AI Governance Engine", "/phase9/governance_enforce", "GET", null],
  ["SAFE AI Bias + Drift Oversight Engine", "/phase9/bias_drift_oversight_check", "GET", null],
  ["SAFE AI Adaptive Guardrails", "/phase9/adaptive_guardrails_guard", "GET", null],
  ["AI static 'Black Box' Monitoring Visualizer", "/phase9/black_box_monitoring_visualize", "GET", null],
  ["AI static Guardrail Consistency Validator", "/phase9/guardrail_consistency_validate", "GET", null],
  ["AI static Multi-Agent Output Concordance Checker", "/phase9/multi_agent_output_concordance_check", "GET", null],
  // Organic Empire Growth Support
  ["AI static 'Blue Ocean' Niche Finder", "/phase9/blue_ocean_niche_find", "GET", null],
  ["AI static Cross-Industry Vault Planner", "/phase9/cross_industry_vault_plan", "GET", null],
  ["AI static Market Adjacency Bridge Engine", "/phase9/market_adjacency_bridge", "GET", null],
  ["AI static Global Expansion Readiness Map", "/phase9/global_expansion_readiness_map", "GET", null],
  ["AI static Brand Equity Trend Tracker", "/phase9/brand_equity_trend_track", "GET", null],
  // Prioritized Features
  ["AI static Industry Disruption Radar", "/phase9/industry_disruption_radar_scan", "GET", null],
  ["AI static Content Differentiation Map", "/phase9/content_differentiation_map", "GET", null],
  ["AI static Strategic Defense Planner", "/phase9/strategic_defense_plan", "GET", null],
  ["AI static External Reputation Monitor", "/phase9/external_reputation_monitor", "GET", null],
  ["AI static PR Risk Early Warning Scanner", "/phase9/pr_risk_early_warning_scan", "GET", null],
  ["AI static Partnership Fit Evaluator", "/phase9/partnership_fit_evaluate", "GET", null],
  // Other Feature Prioritizations
  ["Multi-Org AI Reputation Dashboard", "/phase9/multi_org_ai_reputation_dashboard", "GET", null],
  ["Vault 'Lifespan Health' Tracking Engine", "/phase9/vault_lifespan_health_track", "GET", null],
  ["AI static Cross-Market Trend Amplifier", "/phase9/cross_market_trend_amplify", "GET", null],
  ["Empire-Level Competitive Index Generator", "/phase9/empire_level_competitive_index_generate", "GET", null],
  ["Market Volatility Sensitivity Scanner", "/phase9/market_volatility_sensitivity_scan", "GET", null],
  ["AI static Internationalization Readiness Planner", "/phase9/internationalization_readiness_plan", "GET", null],
];

export default function Phase9StaticModulesPanel() {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState({});
  const [errors, setErrors] = useState({});
  const [apiKey, setApiKey] = useState(localStorage.getItem('phase9_api_key') || 'PHASE9SAFEKEY');
  const [payloads, setPayloads] = useState(() => {
    const initial = {};
    MODULE_API_MAP.forEach(([, , method, payload], idx) => {
      if (method === 'POST') {
        initial[idx] = JSON.stringify(payload, null, 2);
      }
    });
    return initial;
  });

  const handlePayloadChange = (idx, val) => {
    setPayloads(p => ({ ...p, [idx]: val }));
  };

  const handleApiKeyChange = (e) => {
    setApiKey(e.target.value);
    localStorage.setItem('phase9_api_key', e.target.value);
  };

  const runModule = async (idx, endpoint, method, payload) => {
    setLoading(l => ({ ...l, [idx]: true }));
    setErrors(e => ({ ...e, [idx]: null }));
    setResults(r => ({ ...r, [idx]: null }));
    try {
      const url = `http://localhost:8090${endpoint}`;
      let resp;
      const headers = { 'Authorization': `Bearer ${apiKey}` };
      if (method === "GET") {
        resp = await fetch(url, { headers });
      } else {
        let parsedPayload = {};
        try {
          parsedPayload = JSON.parse(payloads[idx]);
        } catch (e) {
          throw new Error('Invalid JSON payload');
        }
        resp = await fetch(url, {
          method: "POST",
          headers: { ...headers, "Content-Type": "application/json" },
          body: JSON.stringify(parsedPayload)
        });
      }
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      setResults(r => ({ ...r, [idx]: data }));
    } catch (err) {
      setErrors(e => ({ ...e, [idx]: String(err) }));
    } finally {
      setLoading(l => ({ ...l, [idx]: false }));
    }
  };

  return (
    <div>
      <h2>Phase 9+ SAFE AI Empire Modules</h2>
      <div style={{marginBottom: 24}}>
        <label style={{fontWeight: 500}}>API Key: </label>
        <input
          type="text"
          value={apiKey}
          onChange={handleApiKeyChange}
          style={{width: 320, padding: 4, fontSize: 15, marginLeft: 8}}
          placeholder="Enter API Key"
        />
      </div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {MODULE_API_MAP.map(([name, endpoint, method, payload], idx) => (
          <li key={idx} style={{ marginBottom: 18, padding: 12, border: '1px solid #eee', borderRadius: 6 }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
              <span style={{ flex: 1 }}>{name}</span>
              {method === 'POST' && (
                <textarea
                  value={payloads[idx]}
                  onChange={e => handlePayloadChange(idx, e.target.value)}
                  rows={4}
                  style={{ fontFamily: 'monospace', fontSize: 13, width: 280, marginRight: 10 }}
                />
              )}
              <button
                onClick={() => runModule(idx, endpoint, method, payload)}
                disabled={loading[idx]}
                style={{ padding: '4px 18px', marginTop: method === 'POST' ? 8 : 0 }}>
                {loading[idx] ? 'Running...' : 'Run'}
              </button>
            </div>
            {errors[idx] && <div style={{ color: 'red', marginTop: 6 }}>Error: {errors[idx]}</div>}
            {results[idx] && (
              <pre style={{ background: '#f8f8f8', fontSize: 13, marginTop: 6, padding: 8, borderRadius: 4 }}>{JSON.stringify(results[idx], null, 2)}</pre>
            )}
          </li>
        ))}
      </ul>
      <p style={{ fontSize: '0.9em', color: '#888', marginTop: 24 }}>
        All modules are static-only, SAFE AI Charter compliant, auditable, and require human approval for all key outputs.
      </p>
    </div>
  );
}
