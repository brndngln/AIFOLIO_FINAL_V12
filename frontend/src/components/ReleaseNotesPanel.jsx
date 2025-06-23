import React from "react";

const NOTES = [
  {date: "2025-06-22", note: "Full launch: static, deterministic, business-only SAFE AI dashboard with PWA support, policy docs, onboarding, and compliance panels."},
  {date: "2025-06-21", note: "Added static safeguard, compliance, and future enhancements panels."},
  {date: "2025-06-20", note: "Removed all global, treaty, and public features. BUSINESS MODE enforced."}
];

export default function ReleaseNotesPanel() {
  return (
    <section aria-labelledby="release-notes-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="release-notes-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Release Notes</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        {NOTES.map((item,i) => (
          <li key={i} style={{marginBottom:8}}><b>{item.date}:</b> {item.note}</li>
        ))}
      </ul>
    </section>
  );
}
