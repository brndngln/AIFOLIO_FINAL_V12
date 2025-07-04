import React from "react";

const RELEASE_NOTES = [
  {
    date: "2025-06-22",
    title: "Full Static OWNER System Launch",
    notes: [
      "All business panels static, deterministic, OWNER-controlled.",
      "Export All Data and onboarding automation complete.",
      "Accessibility and compliance checklists for OWNER.",
      "Policy docs, logs, and branding fully static and PWA-ready."
    ]
  },
  {
    date: "2025-06-15",
    title: "SAFE AI Compliance Panels Added",
    notes: [
      "Static GDPR, tax, audit, and compliance panels.",
      "Beginner Mistakes and Static Logic Suggestions for OWNER.",
      "CI/CD workflow for static deploy and audit."
    ]
  }
];

export default function OwnerReleaseNotesPanel() {
  return (
    <section aria-labelledby="release-notes-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="release-notes-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>Release Notes / Changelog</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Release notes" title="View static release notes and changelog for OWNER business system." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <ul style={{listStyle:'none',padding:0,fontSize:15}} aria-label="Release notes list">
        {RELEASE_NOTES.map((entry, i) => (
          <li key={i} style={{marginBottom:24}}>
            <b style={{color:'#0ea5e9'}}>{entry.date}</b> — <span style={{fontWeight:700}}>{entry.title}</span>
            <ul style={{marginTop:6,marginLeft:20,padding:0}}>
              {entry.notes.map((n, j) => (
                <li key={j} style={{color:'#64748b',marginBottom:4}}>{n}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </section>
  );
}
