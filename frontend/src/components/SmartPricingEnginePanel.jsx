import React from "react";

export default function SmartPricingEnginePanel() {
  const features = [
    { label: "Manual Price Lock", desc: "OWNER can set/lock price" },
    { label: "Value-Based Pricing Engine", desc: "Static value-based price suggestion" },
    { label: "Bundle Logic Engine", desc: "Static bundle price logic" },
    { label: "Niche Multiplier Engine", desc: "Static multiplier for niche vaults" },
    { label: "Competitive Intelligence Engine", desc: "Static stub (no adaptive scraping)" },
    { label: "Psychological Pricing Engine", desc: "Static price rounding/psychological cues" },
    { label: "Tier-Based Engine", desc: "Static tier logic (Basic/Pro/Enterprise)" },
    { label: "Performance Optimizer Engine", desc: "Static stub for performance notes" }
  ];
  return (
    <section aria-labelledby="smart-pricing-engine-heading" style={{background:'#f1f5f9',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #dbeafe'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="smart-pricing-engine-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:24,margin:0}}>Autonomous Smart Pricing Engine</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the Smart Pricing Engine?" title="This engine statically suggests and validates pricing logic. No adaptive or sentient pricing." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="Smart pricing engine features">
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
