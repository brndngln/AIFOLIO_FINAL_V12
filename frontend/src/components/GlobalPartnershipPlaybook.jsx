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
export default function GlobalPartnershipPlaybook() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:20, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#2563eb', fontWeight:600, marginBottom:8}}>SAFE AI GLOBAL PARTNERSHIP PLAYBOOK</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:14}}>
        {PLAYBOOK.map((item, i) => (
          <li key={i} style={{marginBottom:6}}><span style={{color:'#2563eb', fontWeight:500}}>✔</span> {item}</li>
        ))}
      </ul>
    </div>
  );
}
