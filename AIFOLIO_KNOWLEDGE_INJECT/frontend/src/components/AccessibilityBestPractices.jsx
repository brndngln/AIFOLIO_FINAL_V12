import React from "react";

export default function AccessibilityBestPractices() {
  return (
    <section aria-labelledby="accessibility-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="accessibility-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Accessibility Best Practices</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Use keyboard navigation for all dashboard actions</li>
        <li>All buttons and panels have ARIA labels and roles</li>
        <li>Color contrast and large clickable areas for all controls</li>
        <li>Skip-to-content link for screen readers</li>
        <li>All panels and checklists are accessible and readable</li>
        <li>All interactive elements have focus and hover styles</li>
      </ul>
    </section>
  );
}
