import React from "react";

export default function EmailHealthReportPanel() {
  return (
    <section aria-labelledby="email-health-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="email-health-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Email Health Report</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static report of email delivery health (bounced, flagged, success)</li>
        <li>OWNER can review and export report</li>
        <li>No adaptive/AI analytics</li>
      </ul>
    </section>
  );
}
