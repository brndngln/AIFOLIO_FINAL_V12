import React from "react";

export default function NewCountryTaxLawsWatchPanel() {
  return (
    <section aria-labelledby="new-country-tax-laws-heading" style={{background:'#f3f4f6',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #cbd5e1'}}>
      <h3 id="new-country-tax-laws-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>New Country Tax Laws Watch</h3>
      <ul style={{fontSize:15,margin:0,padding:0,listStyle:'none'}}>
        <li>Static tracker for new tax laws by country</li>
        <li>OWNER can log and review new tax law changes</li>
        <li>All logic is static, deterministic, and non-adaptive</li>
      </ul>
    </section>
  );
}
