// Phase 8 SAFE AI Static Modules Panel
// Shows audit logs for all Phase 8 modules
import React, { useState, useEffect } from "react";

const MODULES = [
  { name: "Global Failover", endpoint: "/api/phase8/global_failover_log" },
  {
    name: "Multi-Cloud Deployment",
    endpoint: "/api/phase8/multi_cloud_deployment_log",
  },
  { name: "Load Forecasting", endpoint: "/api/phase8/load_forecasting_log" },
  { name: "Geo Latency Optimizer", endpoint: "/api/phase8/geo_latency_log" },
  {
    name: "Distributed Pipeline",
    endpoint: "/api/phase8/distributed_pipeline_log",
  },
  {
    name: "Multi-Agent Load Balancer",
    endpoint: "/api/phase8/multi_agent_load_balancer_log",
  },
  { name: "AI Self-Audit", endpoint: "/api/phase8/ai_self_audit_log" },
  { name: "Black Box Anomaly", endpoint: "/api/phase8/black_box_anomaly_log" },
  { name: "AI Test Sandbox", endpoint: "/api/phase8/ai_test_sandbox_log" },
  { name: "Bias Trend Monitor", endpoint: "/api/phase8/bias_trend_log" },
  {
    name: "Drift Detection Monitor",
    endpoint: "/api/phase8/drift_detection_log",
  },
  {
    name: "Market Adjacency Map",
    endpoint: "/api/phase8/market_adjacency_map_log",
  },
  {
    name: "Vault Meta-Market Map",
    endpoint: "/api/phase8/vault_meta_market_log",
  },
  {
    name: "Competitor Intelligence",
    endpoint: "/api/phase8/competitor_intel_log",
  },
  {
    name: "Ecosystem Health Monitor",
    endpoint: "/api/phase8/ecosystem_health_log",
  },
  { name: "Threat Radar", endpoint: "/api/phase8/threat_radar_log" },
  {
    name: "Price Sensitivity Map",
    endpoint: "/api/phase8/price_sensitivity_map_log",
  },
  {
    name: "Buyer Sentiment Explorer",
    endpoint: "/api/phase8/buyer_sentiment_log",
  },
  {
    name: "Revenue Curve Forecaster",
    endpoint: "/api/phase8/revenue_curve_forecast_log",
  },
  {
    name: "Cashflow Projection Engine",
    endpoint: "/api/phase8/cashflow_projection_log",
  },
  { name: "Vault Financial P&L Engine", endpoint: "/api/phase8/vault_pnl_log" },
  { name: "Refund Risk Scanner", endpoint: "/api/phase8/refund_risk_scan_log" },
  {
    name: "Regional Profitability Map",
    endpoint: "/api/phase8/regional_profitability_log",
  },
  { name: "Compliance Tree", endpoint: "/api/phase8/compliance_tree_log" },
  { name: "Global Tax Sync", endpoint: "/api/phase8/global_tax_sync_log" },
  {
    name: "Regulatory Horizon Scanner",
    endpoint: "/api/phase8/regulatory_horizon_log",
  },
  { name: "IP Violation Monitor", endpoint: "/api/phase8/ip_violation_log" },
  {
    name: "Data Sovereignty Monitor",
    endpoint: "/api/phase8/data_sovereignty_log",
  },
  {
    name: "Public Complaint Risk Detector",
    endpoint: "/api/phase8/public_complaint_risk_log",
  },
  {
    name: "Buyer Journey Visualizer",
    endpoint: "/api/phase8/buyer_journey_log",
  },
  {
    name: "Loyalty Program Planner",
    endpoint: "/api/phase8/loyalty_program_log",
  },
  {
    name: "Referral Engine Optimizer",
    endpoint: "/api/phase8/referral_engine_log",
  },
  { name: "Content Gap Finder", endpoint: "/api/phase8/content_gap_log" },
  { name: "Future Vault Planner", endpoint: "/api/phase8/future_vault_log" },
  {
    name: "Cross-Market Promotion Planner",
    endpoint: "/api/phase8/cross_market_promo_log",
  },
  {
    name: "Seasonal Campaign Optimizer",
    endpoint: "/api/phase8/seasonal_campaign_log",
  },
  {
    name: "Revenue Reconciliation",
    endpoint: "/api/phase8/revenue_reconciliation_log",
  },
  {
    name: "Vault Lifecycle Intelligence",
    endpoint: "/api/phase8/vault_lifecycle_log",
  },
  {
    name: "Cold Vault Detection",
    endpoint: "/api/phase8/cold_vault_detection_log",
  },
  {
    name: "Archive Optimization Bot",
    endpoint: "/api/phase8/archive_optimization_log",
  },
  {
    name: "Supply-Demand Imbalance Monitor",
    endpoint: "/api/phase8/supply_demand_imbalance_log",
  },
  {
    name: "Legal Event Watcher",
    endpoint: "/api/phase8/legal_event_watch_log",
  },
  {
    name: "AI Safety Signature Verifier",
    endpoint: "/api/phase8/ai_safety_signature_log",
  },
  {
    name: "Customer Satisfaction Map",
    endpoint: "/api/phase8/customer_satisfaction_log",
  },
  {
    name: "External Channel Risk Monitor",
    endpoint: "/api/phase8/external_channel_risk_log",
  },
  {
    name: "Customer Segment Discovery",
    endpoint: "/api/phase8/customer_segment_log",
  },
];

function Phase8StaticModulesPanel() {
  const [logs, setLogs] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all(
      MODULES.map((mod) =>
        fetch(mod.endpoint)
          .then((res) => res.json())
          .then((data) => ({ name: mod.name, data }))
          .catch(() => ({ name: mod.name, data: ["Error loading log"] })),
      ),
    ).then((results) => {
      const logMap = {};
      results.forEach((r) => {
        logMap[r.name] = r.data;
      });
      setLogs(logMap);
      setLoading(false);
    });
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h2>Phase 8 SAFE AI Static Modules Audit Logs</h2>
      {loading && <div>Loading logs...</div>}
      {!loading && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 24 }}>
          {MODULES.map((mod) => (
            <div
              key={mod.name}
              style={{
                minWidth: 320,
                background: "#f9f9f9",
                borderRadius: 8,
                boxShadow: "0 2px 8px #eee",
                padding: 16,
              }}
            >
              <h3 style={{ marginBottom: 8 }}>{mod.name}</h3>
              <pre
                style={{
                  maxHeight: 180,
                  overflow: "auto",
                  background: "#222",
                  color: "#b8f",
                }}
              >
                {(logs[mod.name] || []).join("\n")}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Phase8StaticModulesPanel;
