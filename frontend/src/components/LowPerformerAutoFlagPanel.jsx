import React from "react";

export default function LowPerformerAutoFlagPanel() {
  return (
    <section aria-labelledby="low-performer-flag-heading" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #e0e7ef'}}>
      <h3 id="low-performer-flag-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Low Performing Vault Auto-Flag</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static flag for vaults with low sales or engagement</li>
        <li>OWNER can review and take action on flagged vaults</li>
        <li>All logic is static and deterministic</li>
      </ul>
    </section>
  );
}
