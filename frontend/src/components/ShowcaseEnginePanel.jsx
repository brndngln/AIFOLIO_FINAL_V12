import React from "react";

export default function ShowcaseEnginePanel() {
  return (
    <section aria-labelledby="showcase-engine-heading" style={{background:'#f8fafc',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <h2 id="showcase-engine-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:24,marginBottom:12}}>Autonomous Showcase Engine</h2>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li><b>Outline Generator:</b> Static outline auto-generated from vault metadata</li>
        <li><b>PDF Screenshot Preview Generator:</b> Static preview (watermarked/blurred, OWNER uploads image)</li>
        <li><b>Testimonial Generator:</b> OWNER-editable, capped at 40</li>
        <li><b>Realistic Review Engine:</b> Static, deterministic reviews (no adaptation)</li>
        <li><b>AI Benefit Copy Generator:</b> OWNER-editable, static benefit copy</li>
        <li><b>Vault Value Score Engine:</b> Static score (0–100) based on metadata</li>
        <li><b>vault_preview.json Auto-Compiler:</b> Static UI for creating/validating preview.json</li>
        <li><b>Blocks upload if missing preview/testimonial/screenshot</b></li>
      </ul>
    </section>
  );
}
