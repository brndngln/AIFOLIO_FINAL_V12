import React from "react";

export default function GDPRDashboardPanel() {
  return (
    <section aria-labelledby="gdpr-dashboard-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="gdpr-dashboard-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>GDPR Request Dashboard</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static dashboard for access/delete GDPR requests</li>
        <li>OWNER can log and export GDPR requests</li>
        <li>All actions are statically audit-logged</li>
      </ul>
    </section>
  );
}
