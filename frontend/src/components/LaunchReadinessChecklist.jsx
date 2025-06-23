import React from "react";

const CHECKLIST = [
  "App icons replaced with AIFOLIO™ branding",
  "PWA install tested on Mac and phone",
  "All policy docs reviewed in dashboard",
  "All business-only panels present (no global/public features)",
  "Sample/test vaults reviewed",
  "Static build deployed to Netlify/Vercel/static host",
  "CI/CD workflow set up (optional)",
  "Accessibility and onboarding reviewed"
];

export default function LaunchReadinessChecklist() {
  return (
    <section aria-labelledby="launch-readiness-heading" style={{background:'#f0fdfa',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #bae6fd'}}>
      <h3 id="launch-readiness-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Launch Readiness Checklist</h3>
      <ul style={{listStyle:'none',padding:0,fontSize:15}}>
        {CHECKLIST.map((item,i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#0ea5e9',fontWeight:600}}>✔</span> {item}</li>
        ))}
      </ul>
    </section>
  );
}
