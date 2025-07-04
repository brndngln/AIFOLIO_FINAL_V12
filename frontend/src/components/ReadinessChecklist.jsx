<<<<<<< HEAD
import React from "react";
=======
// [WINDSURF FIXED ✅]
import React from "react";
import PropTypes from 'prop-types'; // [WINDSURF FIXED]
>>>>>>> omni_repair_backup_20250704_1335
const BUSINESS = [
  "All regulatory requirements mapped",
  "GDPR/CCPA compliance",
  "Partner certification complete",
  "Owner-controlled export only",
  "Audit-logging enabled",
  "No adaptive or marketing features"
];
<<<<<<< HEAD
=======
const AIFOLIO = [
  "Vault structure validated",
  "All AI modules locked non-sentient",
  "Owner override on all exports",
  "PDF automation pipelines tested",
  "Compliance audit complete"
];

>>>>>>> omni_repair_backup_20250704_1335
const PUBLIC = [
  "Public trust badge system present",
  "Public/partner exports OWNER-controlled",
  "No auto-publicity or dynamic dashboards",
  "Public reporting static and deterministic",
  "Global governance alignment exportable"
];
<<<<<<< HEAD
export default function ReadAIFOLIOChecklist() {
=======
function ReadAIFOLIOChecklist() {
>>>>>>> omni_repair_backup_20250704_1335
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:20, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#2563eb', fontWeight:600, marginBottom:8}}>SAFE AI READINESS CHECKLIST</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:14, marginBottom:16}}>
        {AIFOLIO.map((item, i) => (
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
<<<<<<< HEAD
=======

// No props for ReadAIFOLIOChecklist; PropTypes not required. [WINDSURF FIXED]

// [WINDSURF FIXED ✅]
export default ReadAIFOLIOChecklist; // [WINDSURF FIXED]

>>>>>>> omni_repair_backup_20250704_1335
