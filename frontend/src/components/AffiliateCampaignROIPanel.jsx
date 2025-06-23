import React from "react";

export default function AffiliateCampaignROIPanel() {
  return (
    <section aria-labelledby="affiliate-roi-heading" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #e0e7ef'}}>
      <h3 id="affiliate-roi-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Affiliate Campaign ROI Tracker</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static panel for tracking affiliate campaign ROI</li>
        <li>OWNER can log and export affiliate campaign results</li>
        <li>No adaptive/AI marketing logic</li>
      </ul>
    </section>
  );
}
