import React from "react";

export default function VaultPreviewCompilerPanel() {
  return (
    <section aria-labelledby="vault-preview-compiler-heading" style={{background:'#f8fafc',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <h2 id="vault-preview-compiler-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:24,marginBottom:12}}>vault_preview.json Auto-Compiler</h2>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static UI for creating and validating <code>vault_preview.json</code></li>
        <li>Blocks upload if any preview/testimonial/screenshot is missing</li>
        <li>OWNER-controlled: all edits and exports require explicit OWNER action</li>
        <li>Audit-log of all preview.json changes (static, visible to OWNER)</li>
      </ul>
      <div style={{marginTop:18,background:'#e0e7ef',padding:12,borderRadius:8}}>
        <b>Sample preview.json location:</b> <code>src/sample-data/sample_vault_preview.json</code>
      </div>
    </section>
  );
}
