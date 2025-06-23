import React from "react";

export default function ComplianceExportsPanel() {
  const features = [
    { label: "Export compliance logs", desc: "Export logs as PDF, CSV, or XBRL (static sample)" },
    { label: "OWNER-controlled export", desc: "Only OWNER can export compliance data" }
  ];
  return (
    <section aria-labelledby="compliance-exports-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
        <h3 id="compliance-exports-heading" style={{color:'#0ea5e9',fontWeight:700,margin:0}}>Compliance Export</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is Compliance Export?" title="OWNER can export static compliance logs for audits. No adaptive logic." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}} aria-label="Compliance export features">
        {features.map((f, i) => (
          <li key={i} style={{marginBottom:8,display:'flex',alignItems:'center',gap:8}}>
            <span style={{color:'#0ea5e9', fontWeight:600}} aria-label="Feature">•</span>
            <span tabIndex={0} aria-label={f.label} title={f.desc}>{f.label}: {f.desc}</span>
            <span tabIndex={0} aria-label="Help" title={f.desc} style={{color:'#64748b',cursor:'help',fontWeight:800,fontSize:15}}>?</span>
          </li>
        ))}
      </ul>
      <button
        style={{background:'#0ea5e9',color:'#fff',border:'none',borderRadius:6,padding:'10px 20px',fontWeight:700,fontSize:15,cursor:'pointer',marginTop:12,boxShadow:'0 1px 2px #bae6fd'}}
        aria-label="Download compliance export"
        onClick={()=>window.open('/analytics/pricing_log.json','_blank')}
      >
        Download Compliance Export (Sample)
      </button>
    </section>
  );
}
