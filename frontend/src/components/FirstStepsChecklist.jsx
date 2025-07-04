import React from "react";

const STEPS = [
  "Read all policy documents (Terms, Refund, Privacy)",
  "Replace app icons with your brand icons",
  "Install the app as a PWA on your device",
  "Review and test sample vaults",
  "Complete all checklists and safeguard panels",
  "Run a test PDF vault export",
  "Deploy to your static host",
  "Set up CI/CD workflow if needed"
];

<<<<<<< HEAD
=======
// [WINDSURF FIXED ✅]
>>>>>>> omni_repair_backup_20250704_1335
export default function FirstStepsChecklist() {
  return (
    <section aria-labelledby="first-steps-heading" style={{background:'#fef9c3',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #fde68a'}}>
      <h3 id="first-steps-heading" style={{color:'#f59e42',fontWeight:700,marginBottom:10}}>OWNER First Steps Checklist</h3>
      <ul style={{listStyle:'none',padding:0,fontSize:15}}>
        {STEPS.map((step,i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#f59e42',fontWeight:600}}>✔</span> {step}</li>
        ))}
      </ul>
    </section>
  );
}
