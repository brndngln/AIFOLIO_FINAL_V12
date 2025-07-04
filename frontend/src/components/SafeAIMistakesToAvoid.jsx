import React from "react";

// List of critical mistakes to avoid for OWNER compliance and deterministic SAFE AI
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

// [WINDSURF FIXED ✅]
export default function SafeAIMistakesToAvoid() {
  return (
    <section aria-labelledby="safe-ai-mistakes-heading" style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h3 id="safe-ai-mistakes-heading" style={{color:'#ef4444', fontWeight:700, margin:0}}>SAFE AI — Beginner Mistakes to Avoid</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Why these mistakes matter" title="Each mistake can break SAFE AI compliance, audit, or trust. OWNER must avoid all for deterministic, compliant business mode." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{listStyle:'none', padding:0, fontSize:15}} aria-label="SAFE AI mistakes list">
        {MISTAKES.map((item, i) => (
          <li key={i} style={{marginBottom:8,display:'flex',alignItems:'center',gap:8}}>
            <span style={{color:'#ef4444', fontWeight:600}} aria-label="Not allowed">✘</span>
            <span tabIndex={0} aria-label={`Mistake: ${item}`} title={`Why avoid: ${item}`}>{item}</span>
            <span tabIndex={0} aria-label="Help" title="Click for explanation" style={{color:'#64748b',cursor:'help',fontWeight:800,fontSize:15}}></span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> Avoid all above mistakes to maintain SAFE AI compliance and trust.
      </div>
    </section>
  );
}
