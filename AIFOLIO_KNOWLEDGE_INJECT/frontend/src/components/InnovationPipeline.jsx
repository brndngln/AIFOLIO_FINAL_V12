import React from "react";

const PIPELINE = [
  "Static feature queue for future SAFE AI modules",
  "Manual prioritization by OWNER only",
  "No adaptive or learning logic",
  "Audit-logged feature approvals",
  "Static compliance review for all pipeline items",
  "Annual pipeline review (static)",
  "OWNER can export pipeline report"
];

// [WINDSURF FIXED ✅]
export default function InnovationPipeline() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#fbbf24', fontWeight:700, marginBottom:12}}>SAFE AI Innovation Pipeline</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:15}}>
        {PIPELINE.map((item, i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#fbbf24', fontWeight:600}}>★</span> {item}</li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> All pipeline actions are static, audit-logged, and require OWNER approval.
      </div>
    </div>
  );
}
