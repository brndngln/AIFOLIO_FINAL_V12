import React from "react";

export default function ShowcaseEnginePanel() {
  const features = [
    { label: "Outline Generator", desc: "Static outline auto-generated from vault metadata" },
    { label: "PDF Screenshot Preview Generator", desc: "Static preview (watermarked/blurred, OWNER uploads image)" },
    { label: "Testimonial Generator", desc: "OWNER-editable, capped at 40" },
    { label: "Realistic Review Engine", desc: "Static, deterministic reviews (no adaptation)" },
    { label: "AI Benefit Copy Generator", desc: "OWNER-editable, static benefit copy" },
    { label: "Vault Value Score Engine", desc: "Static score (0–100) based on metadata" },
    { label: "vault_preview.json Auto-Compiler", desc: "Static UI for creating/validating preview.json" },
    { label: "Blocks upload if missing preview/testimonial/screenshot", desc: "Prevents incomplete vaults from being published" }
  ];
  return (
    <section aria-labelledby="showcase-engine-heading" style={{background:'#f8fafc',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="showcase-engine-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:24,margin:0}}>Autonomous Showcase Engine</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the Showcase Engine?" title="This engine statically generates all showcase content for OWNER review. No adaptive or sentient logic." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="Showcase engine features">
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
