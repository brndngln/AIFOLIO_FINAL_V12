import React from "react";

export default function GDPRDashboardPanel() {
  const features = [
    { label: "Static GDPR dashboard", desc: "Dashboard for access/delete GDPR requests" },
    { label: "OWNER can log/export", desc: "OWNER can log and export GDPR requests" },
    { label: "Audit-logged actions", desc: "All actions are statically audit-logged" }
  ];
  return (
    <section aria-labelledby="gdpr-dashboard-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
        <h3 id="gdpr-dashboard-heading" style={{color:'#0ea5e9',fontWeight:700,margin:0}}>GDPR Request Dashboard</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the GDPR Dashboard?" title="Static, deterministic GDPR request log. OWNER controls all exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="GDPR dashboard features">
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
