import React from "react";

export default function TaxFilingCalendarPanel() {
  return (
    <section aria-labelledby="tax-filing-calendar-heading" style={{background:'#f8fafc',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #e0e7ef'}}>
      <h3 id="tax-filing-calendar-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Tax Filing Calendar</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static calendar of tax deadlines for business vaults</li>
        <li>OWNER can add, edit, or export deadlines</li>
        <li>All logic is static, deterministic, and non-adaptive</li>
      </ul>
    </section>
  );
}
