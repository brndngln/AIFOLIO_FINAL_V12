import React from "react";

const SUGGESTIONS = [
  "Static Anomaly Detector — reports sudden changes in partner activity (manual input)",
  "Static Regulatory Changes Monitor — flags known law changes (manual update)",
  "Static Ecosystem Coverage Heatmap — shows partner category coverage (static data)",
  "Static Vault Success Predictor — based on static sales trends (no learning)",
  "Static Cross-Partner Opportunity Map (static)",
  "Static Revenue Impact Estimator for Market Changes (static)",
  "Static Compliance Drift Detector (manual input)",
  "Static Public Sentiment Tracker — manual-input only",
  "Static High-Impact Vault Clustering (non-adaptive)",
  "Static Cross-Market Vault Linker (static)"
];

const suggestions = [
  { label: "Deterministic logic only", desc: "Use only deterministic, non-adaptive logic in all business flows" },
  { label: "OWNER approval required", desc: "OWNER must approve all logic changes before deploy" },
  { label: "Document and audit", desc: "Document all static logic and audit changes" },
  { label: "No adaptive/agentic AI", desc: "Never allow adaptive or agentic AI in SAFE AI mode" },
  { label: "OWNER-controlled outputs", desc: "All exports and outputs must be OWNER-controlled" }
];

export default function SafeAIStaticLogicSuggestions() {
  return (
    <section aria-labelledby="static-logic-suggestions-heading" style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h3 id="static-logic-suggestions-heading" style={{color:'#0ea5e9', fontWeight:700, margin:0}}>SAFE AI — Static Logic Suggestions</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What are Static Logic Suggestions?" title="These are OWNER rules for SAFE AI compliance. All logic must be static, deterministic, and OWNER-controlled." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{listStyle:'none', padding:0, fontSize:15}} aria-label="SAFE AI static logic suggestions list">
        {suggestions.map((s, i) => (
          <li key={i} style={{marginBottom:8,display:'flex',alignItems:'center',gap:8}}>
            <span style={{color:'#0ea5e9', fontWeight:600}} aria-label="Suggestion">•</span>
            <span tabIndex={0} aria-label={s.label} title={s.desc}>{s.label}: {s.desc}</span>
            <span tabIndex={0} aria-label="Help" title={s.desc} style={{color:'#64748b',cursor:'help',fontWeight:800,fontSize:15}}>?</span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> Follow all above logic rules for SAFE AI compliance.
      </div>
    </section>
  );
}
