import React from "react";

export default function UpcomingVaultsPipelinePanel() {
  return (
    <section aria-labelledby="upcoming-vaults-heading" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #e0e7ef'}}>
      <h3 id="upcoming-vaults-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Upcoming Vaults Pipeline</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static viewer for upcoming vaults in the pipeline</li>
        <li>OWNER can add, edit, or archive pipeline entries</li>
        <li>All actions are statically audit-logged</li>
      </ul>
    </section>
  );
}
