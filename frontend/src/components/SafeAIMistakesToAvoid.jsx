import React from "react";

const MISTAKES = [
  "Forgetting to log public/partner exports",
  "Auto-publishing by mistake",
  "Using adaptive marketing AI with SAFE AI",
  "Letting experimental AI touch SAFE AI core",
  "Forgetting GDPR / CCPA opt-outs",
  "Skipping SAFE AI UX Best Practices",
  "Deploying unverified dashboards",
  "Forgetting OWNER approval on public/partner outputs",
  "Letting frontend introduce non-deterministic elements",
  "Missing audit log entries for public-facing outputs"
];

export default function SafeAIMistakesToAvoid() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#ef4444', fontWeight:700, marginBottom:12}}>SAFE AI — Beginner Mistakes to Avoid</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:15}}>
        {MISTAKES.map((item, i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#ef4444', fontWeight:600}}>✘</span> {item}</li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> Avoid all above mistakes to maintain SAFE AI compliance and trust.
      </div>
    </div>
  );
}
