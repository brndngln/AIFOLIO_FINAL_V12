import React from "react";

const TREATIES = [
  "OECD AI Principles",
  "UNESCO AI Ethics Recommendation",
  "EU AI Act",
  "UN AI Advisory Body Recommendations",
  "US AI Executive Orders",
  "G7 Hiroshima AI Process",
  "Global Partnership on AI (GPAI)",
  "OECD AI Policy Observatory",
  "UN AI for Good Summit",
  "Other national/international frameworks"
];

export default function TreatyTracker() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:24, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#2563eb', fontWeight:700, marginBottom:12}}>SAFE AI Treaty Tracker</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:15}}>
        {TREATIES.map((item, i) => (
          <li key={i} style={{marginBottom:8}}><span style={{color:'#059669', fontWeight:600}}>✔</span> {item}</li>
        ))}
      </ul>
      <div style={{marginTop:18, color:'#64748b', fontSize:13}}>
        <b>OWNER CONTROLLED:</b> This tracker is static, non-adaptive, and flags if manual updates are needed. Maps to global treaty frameworks.
      </div>
    </div>
  );
}
