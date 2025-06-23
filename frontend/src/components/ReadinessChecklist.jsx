import React from "react";
const BUSINESS = [
  "All regulatory requirements mapped",
  "GDPR/CCPA compliance",
  "Partner certification complete",
  "Owner-controlled export only",
  "Audit-logging enabled",
  "No adaptive or marketing features"
];
const PUBLIC = [
  "Public trust badge system present",
  "Public/partner exports OWNER-controlled",
  "No auto-publicity or dynamic dashboards",
  "Public reporting static and deterministic",
  "Global governance alignment exportable"
];
export default function ReadinessChecklist() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:20, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#2563eb', fontWeight:600, marginBottom:8}}>SAFE AI BUSINESS READINESS CHECKLIST</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:14, marginBottom:16}}>
        {BUSINESS.map((item, i) => (
          <li key={i} style={{marginBottom:6}}><span style={{color:'#2563eb', fontWeight:500}}>✔</span> {item}</li>
        ))}
      </ul>
      <h3 style={{color:'#059669', fontWeight:600, marginBottom:8}}>SAFE AI PUBLIC READINESS CHECKLIST</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:14}}>
        {PUBLIC.map((item, i) => (
          <li key={i} style={{marginBottom:6}}><span style={{color:'#059669', fontWeight:500}}>✔</span> {item}</li>
        ))}
      </ul>
    </div>
  );
}
