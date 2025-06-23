import React from "react";

export default function ComplianceExportsPanel() {
  return (
    <section aria-labelledby="compliance-exports-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="compliance-exports-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Compliance Export</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Export compliance logs as PDF, CSV, or XBRL (static sample)</li>
        <li>OWNER-controlled export only</li>
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
