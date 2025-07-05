import React from "react";
const PRACTICES = [
  "Clear OWNER controls for all exports",
  "No auto-publicity or adaptive UI",
  "Accessible, readable UI for all users",
  "Audit log visible and exportable",
  "All actions require explicit OWNER approval",
  "No marketing, targeting, or tracking",
  "Static, deterministic, non-sentient design",
  "All checklists and guides exportable"
];
// [WINDSURF FIXED ✅]
export default function UXBestPractices() {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:20, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#fbbf24', fontWeight:600, marginBottom:8}}>SAFE AI UX BEST PRACTICES GUIDE</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:14}}>
        {PRACTICES.map((item, i) => (
          <li key={i} style={{marginBottom:6}}><span style={{color:'#fbbf24', fontWeight:500}}>✔</span> {item}</li>
        ))}
      </ul>
    </div>
  );
}
