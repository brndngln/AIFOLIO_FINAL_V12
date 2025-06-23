import React from "react";

export default function PolicyDocuments() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#0ea5e9', fontWeight:700, marginBottom:12}}>POLICY DOCUMENTS</h3>
      <ul style={{fontSize:15, margin:0, padding:0, listStyle:'none'}}>
        <li><b>Terms of Service</b> — Static, business-focused terms for all users</li>
        <li><b>Refund Policy</b> — Clear refund terms for digital vaults</li>
        <li><b>Privacy Policy</b> — GDPR/CCPA compliant, static privacy statement</li>
      </ul>
    </div>
  );
}
