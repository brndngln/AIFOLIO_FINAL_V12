import React from "react";

export default function AudienceInterestHeatmapPanel() {
  return (
    <section aria-labelledby="audience-heatmap-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="audience-heatmap-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Audience Interest Heatmap</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static, sales-based heatmap (no personal tracking)</li>
        <li>OWNER can review interest by vault or tag</li>
        <li>No adaptive analytics or tracking</li>
      </ul>
    </section>
  );
}
