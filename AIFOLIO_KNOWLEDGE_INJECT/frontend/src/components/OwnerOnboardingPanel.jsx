import React, { useState, useEffect } from "react";

const ONBOARDING_STEPS = [
  "Set business name and logo",
  "Review and edit policy docs",
  "Test Export All Data button",
  "Install as PWA on your device",
  "Review OWNER dashboard features",
  "Complete accessibility checklist",
  "Read Release Notes/Changelog"
];

export default function OwnerOnboardingPanel() {
  const [progress, setProgress] = useState(() => {
    const saved = localStorage.getItem("aifolio_onboarding_progress");
    return saved ? JSON.parse(saved) : Array(ONBOARDING_STEPS.length).fill(false);
  });

  useEffect(() => {
    localStorage.setItem("aifolio_onboarding_progress", JSON.stringify(progress));
  }, [progress]);

  const completeCount = progress.filter(Boolean).length;
  const percent = Math.round((completeCount / ONBOARDING_STEPS.length) * 100);

  return (
    <section aria-labelledby="owner-onboarding-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="owner-onboarding-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>OWNER Onboarding Checklist</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Onboarding steps" title="Follow these steps to complete initial setup and compliance." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <div style={{marginBottom:18}} aria-label="Onboarding progress">
        <div style={{height:8,background:'#e5e7eb',borderRadius:4,overflow:'hidden',marginBottom:6}}>
          <div style={{width:`${percent}%`,background:'#0ea5e9',height:8}}></div>
        </div>
        <span style={{fontSize:13,color:'#64748b'}}>{completeCount} of {ONBOARDING_STEPS.length} steps complete</span>
      </div>
      <ul style={{listStyle:'none',padding:0,fontSize:15}} aria-label="Onboarding checklist">
        {ONBOARDING_STEPS.map((step, i) => (
          <li key={i} style={{marginBottom:12,display:'flex',alignItems:'center',gap:8}}>
            <input
              type="checkbox"
              checked={progress[i]}
              aria-label={`Mark step '${step}' as complete`}
              onChange={() => {
                const next = [...progress];
                next[i] = !next[i];
                setProgress(next);
              }}
              style={{accentColor:'#0ea5e9'}}
            />
            <span tabIndex={0} aria-label={`Onboarding step: ${step}`}>{step}</span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:18,color:'#64748b',fontSize:13}}>
        <b>Tip:</b> Progress is saved in your browser. Complete all steps for best OWNER experience.
      </div>
    </section>
  );
}
