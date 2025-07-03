import React from "react";
import HyperEliteVaultBadge from '../../components/HyperEliteVaultBadge';

export default function UpcomingVaultsPipelinePanel() {
  const features = [
    { label: "Static pipeline", desc: "Pipeline for upcoming vaults (future releases, in review, etc)" },
    { label: "OWNER can update/export", desc: "OWNER can update and export pipeline data" },
    { label: "Static, deterministic logic", desc: "All pipeline logic is static, deterministic, and non-adaptive" }
  ];
  return (
    <section aria-labelledby="upcoming-vaults-heading" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
        <h3 id="upcoming-vaults-heading" style={{color:'#0ea5e9',fontWeight:700,margin:0,display:'flex',alignItems:'center',gap:8}}>
  Upcoming Vaults Pipeline
  <HyperEliteVaultBadge tooltip={true} external={false} />
</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the Upcoming Vaults Pipeline?" title="Static, deterministic pipeline for upcoming vaults. OWNER controls all exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="Upcoming vaults features">
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
