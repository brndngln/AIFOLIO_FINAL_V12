import React, { useState } from "react";

const CHECKLIST = [
  "All panels have ARIA labels and roles",
  "All buttons and inputs are keyboard accessible",
  "All tooltips/help icons are accessible via tab",
  "Color contrast meets WCAG 2.1 AA",
  "No flashing or auto-updating UI elements",
  "All OWNER exports are accessible and labeled",
  "All lists and tables use semantic HTML"
];

<<<<<<< HEAD
export default function OwnerAccessibilityChecklistPanel() {
  const [progress, setProgress] = useState(Array(CHECKLIST.length).fill(false));
  const completeCount = progress.filter(Boolean).length;
  const percent = Math.round((completeCount / CHECKLIST.length) * 100);
=======
// [WINDSURF FIXED ✅]
export default function OwnerAccessibilityChecklistPanel() {
  const [progress, setProgress] = useState(Array(CHECKLIST.length).fill(false));
  const completeCount = progress.filter(Boolean).length;
  const percent = Math.round((completeCount / CHECKLIST.length) * 100); // Remove if not used in render or logic
>>>>>>> omni_repair_backup_20250704_1335

  return (
    <section aria-labelledby="accessibility-checklist-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="accessibility-checklist-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>OWNER Accessibility Checklist</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Accessibility checklist" title="OWNER accessibility best practices for all static panels and exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <div style={{marginBottom:18}} aria-label="Accessibility progress">
        <div style={{height:8,background:'#e5e7eb',borderRadius:4,overflow:'hidden',marginBottom:6}}>
          <div style={{width:`${percent}%`,background:'#0ea5e9',height:8}}></div>
        </div>
        <span style={{fontSize:13,color:'#64748b'}}>{completeCount} of {CHECKLIST.length} checks complete</span>
      </div>
      <ul style={{listStyle:'none',padding:0,fontSize:15}} aria-label="Accessibility checklist">
        {CHECKLIST.map((item, i) => (
          <li key={i} style={{marginBottom:12,display:'flex',alignItems:'center',gap:8}}>
            <input
              type="checkbox"
              checked={progress[i]}
              aria-label={`Mark accessibility check '${item}' as complete`}
              onChange={() => {
                const next = [...progress];
                next[i] = !next[i];
                setProgress(next);
              }}
              style={{accentColor:'#0ea5e9'}}
            />
            <span tabIndex={0} aria-label={`Accessibility check: ${item}`}>{item}</span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:18,color:'#64748b',fontSize:13}}>
        <b>Tip:</b> Complete all checks for best OWNER and user accessibility compliance.
      </div>
    </section>
  );
}
