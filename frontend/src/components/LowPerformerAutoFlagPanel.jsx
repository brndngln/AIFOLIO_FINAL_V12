import React from "react";

export default function LowPerformerAutoFlagPanel() {
  const features = [
    { label: "Static auto-flag", desc: "Flag for low-performing vaults (based on static thresholds)" },
    { label: "OWNER can review/approve", desc: "OWNER can review and approve all auto-flags" },
    { label: "Static, deterministic logic", desc: "All logic is static, deterministic, and non-adaptive" }
  ];
  return (
    <section aria-labelledby="auto-flag-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
        <h3 id="auto-flag-heading" style={{color:'#0ea5e9',fontWeight:700,margin:0}}>Low Performer Auto-Flag</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the Auto-Flag?" title="Static, deterministic flag for low-performing vaults. OWNER controls all approvals." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="Auto-flag features">
        {features.map((f, i) => (
          <li key={i} style={{marginBottom:8,display:'flex',alignItems:'center',gap:8}}>
            <span style={{color:'#0ea5e9', fontWeight:600}} aria-label="Feature">•</span>
            <span tabIndex={0} aria-label={f.label} title={f.desc}>{f.label}: {f.desc}</span>
            <span tabIndex={0} aria-label="Help" title={f.desc} style={{color:'#64748b',cursor:'help',fontWeight:800,fontSize:15}}>?</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
