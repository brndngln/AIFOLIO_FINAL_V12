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

export default function SafeAIStaticLogicSuggestions() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#2563eb', fontWeight:700, marginBottom:12}}>SAFE AI Static Logic — Future Suggestions</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:15}}>
        {SUGGESTIONS.map((item, i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#059669', fontWeight:600}}>✔</span> {item}</li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> All features are static, non-sentient, non-adaptive, and require manual input or update. No auto-publish or learning allowed.
      </div>
    </div>
  );
}
