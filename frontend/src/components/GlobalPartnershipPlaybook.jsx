import React from "react";
const PLAYBOOK = [
  "Global partner onboarding checklist",
  "SAFE AI certification for all partners",
  "Cross-national governance alignment",
  "Owner-controlled export of all partnership data",
  "Public/private partner separation",
  "No auto-publish, no adaptive dashboards",
  "Annual partnership review and audit log"
];
const features = [
  { label: "Static business templates", desc: "Static business partnership templates (no global governance)" },
  { label: "OWNER can review/edit/export", desc: "OWNER can review, edit, and export partnership docs" },
  { label: "No adaptive/agentic/treaty logic", desc: "No adaptive, agentic, or treaty logic" },
  { label: "OWNER-controlled and static", desc: "All partnership flows are OWNER-controlled and static" }
];
export default function GlobalPartnershipPlaybook() {
  return (
    <section aria-labelledby="partnership-playbook-heading" style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h3 id="partnership-playbook-heading" style={{color:'#0ea5e9', fontWeight:700, margin:0}}>Global Partnership Playbook</h3>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: What is the Partnership Playbook?" title="Static, AIFOLIO-only partnership templates. No global governance, no adaptive logic." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{listStyle:'none', padding:0, fontSize:15}} aria-label="SAFE AI partnership playbook list">
        {features.map((f, i) => (
          <li key={i} style={{marginBottom:8,display:'flex',alignItems:'center',gap:8}}>
            <span style={{color:'#0ea5e9', fontWeight:600}} aria-label="Feature">•</span>
            <span tabIndex={0} aria-label={f.label} title={f.desc}>{f.label}: {f.desc}</span>
            <span tabIndex={0} aria-label="Help" title={f.desc} style={{color:'#64748b',cursor:'help',fontWeight:800,fontSize:15}}>?</span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> All partnership logic is static, deterministic, and AIFOLIO-only.
      </div>
    </section>
  );
}
