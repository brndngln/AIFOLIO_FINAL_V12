import React, { useState } from "react";

export default function StaticEnhancementsPanel({ apiBase = "http://localhost:PORT", tenantId }) {
  const [result, setResult] = useState({});
  const widgets = [
    { label: "Audience Interest Heatmap", path: "/phase10/analytics/audience_heatmap" },
    { label: "Product Lifecycle Tracker", path: "/phase10/showcase/lifecycle_tracker" },
    { label: "Vault Bundle Recommender", path: "/phase10/showcase/bundle_recommender" },
    { label: "GDPR Request Dashboard", path: "/phase10/compliance/gdpr_dashboard" },
    { label: "Email Health Report", path: "/phase10/analytics/email_health_report" },
    { label: "Tax Filing Calendar", path: "/phase10/compliance/tax_filing_calendar" },
    { label: "New Tax Laws Watch", path: "/phase10/compliance/new_tax_laws_watch" },
    { label: "AI Guard Integrity Monitor", path: "/phase10/ai/guard_integrity_monitor" },
    { label: "Affiliate Campaign ROI Tracker", path: "/phase10/analytics/affiliate_roi_tracker" },
    { label: "Upcoming Vaults Pipeline", path: "/phase10/showcase/upcoming_pipeline" },
    { label: "Low Performance Auto-Flagger", path: "/phase10/analytics/low_performance_auto_flagger" }
  ];
  return (
    <div style={{margin:'32px 0',padding:'18px',border:'1px solid #cde',borderRadius:10,background:'#f7fafd'}}>
      <h3>Static Future Enhancements <span style={{fontSize:13}}>— SAFE AI, deterministic, non-sentient</span></h3>
      <div style={{display:'flex',flexWrap:'wrap',gap:14,marginTop:10}}>
        {widgets.map(w => (
          <button key={w.label} onClick={async()=>{
            const res = await fetch(`${apiBase}${w.path}?tenant_id=${tenantId}`);
            setResult(r=>({...r, [w.label]: await res.json()}));
          }}>{w.label}</button>
        ))}
      </div>
      <div style={{marginTop:18}}>
        {Object.entries(result).map(([label, data]) => (
          <div key={label} style={{marginBottom:12}}>
            <b>{label}:</b>
            <pre style={{background:'#f8fafe',padding:10,borderRadius:6}}>{JSON.stringify(data,null,2)}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}
