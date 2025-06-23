import React, { useState, useEffect } from "react";

export default function OwnerDemoModePanel() {
  const [demo, setDemo] = useState(() => localStorage.getItem("aifolio_demo_mode") === "true");

  useEffect(() => {
    localStorage.setItem("aifolio_demo_mode", demo ? "true" : "false");
  }, [demo]);

  return (
    <section aria-labelledby="demo-mode-heading" style={{background:'#fef9c3',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #fef08a',border:'2px solid #fde047'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="demo-mode-heading" style={{color:'#b45309',fontWeight:800,fontSize:22,margin:0}}>OWNER Demo Mode</h2>
        <span style={{background:'#b45309',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Demo mode" title="Enable Demo Mode for safe demos. Disables all export/destructive actions and shows a warning banner." style={{marginLeft:6, color:'#b45309', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <label style={{display:'flex',alignItems:'center',gap:10,fontWeight:600}}>
        <input
          type="checkbox"
          checked={demo}
          aria-label="Toggle Demo Mode"
          onChange={() => setDemo(!demo)}
          style={{accentColor:'#fde047',width:22,height:22}}
        />
        Enable Demo Mode (safe for presentations; disables export and destructive actions)
      </label>
      {demo && (
        <div style={{marginTop:18,padding:16,background:'#fef08a',borderRadius:8,color:'#b45309',fontWeight:700,fontSize:15}} aria-live="polite">
          <span role="img" aria-label="Warning">⚠️</span> Demo Mode is ON: All export and destructive OWNER actions are disabled for safety.
        </div>
      )}
      <div style={{marginTop:18,color:'#b45309',fontSize:13}}>
        <b>Tip:</b> Use Demo Mode for safe demos and training. Toggle off to restore full OWNER control.
      </div>
    </section>
  );
}
