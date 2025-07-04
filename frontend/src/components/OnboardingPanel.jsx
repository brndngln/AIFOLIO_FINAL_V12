import React from "react";

export default function OnboardingPanel() {
  return (
    <section aria-labelledby="onboarding-heading" style={{background:'#f0fdfa',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0f2fe'}}>
      <h2 id="onboarding-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:28,marginBottom:12}}>Welcome to AIFOLIO SAFE AI Dashboard</h2>
      <p style={{fontSize:16,color:'#334155',marginBottom:10}}>
        This dashboard is static, deterministic, and fully OWNER-controlled. Use the checklist below to get started and ensure your SAFE AI AIFOLIO is compliant and ready for launch.
      </p>
      <ol style={{fontSize:15,marginLeft:18,marginBottom:18}}>
        <li>Review all <b>Policy Documents</b> (Terms, Refund, Privacy) in the Policy panel below.</li>
        <li>Replace default icons in <code>public/</code> with your AIFOLIO™ icons for branding.</li>
<<<<<<< HEAD
        <li>Install as a PWA ("Add to Home Screen") on Mac/phone and test offline support.</li>
=======
        <li>Install as a PWA (&quot;Add to Home Screen&quot;) on Mac/phone and test offline support.</li>
>>>>>>> omni_repair_backup_20250704_1335
        <li>Review sample/test vaults in <code>src/sample-data/</code>.</li>
        <li>Complete all AIFOLIO checklists and safeguard panels.</li>
        <li>Run <code>npm run build</code> and deploy to your static host.</li>
        <li>Set up CI/CD workflow for automated deploys (see README).</li>
      </ol>
      <div style={{marginTop:12,background:'#e0f2fe',padding:12,borderRadius:8}}>
        <b>Need help?</b> See the Support panel below or email <a href="mailto:owner@aifolio.com" style={{color:'#0ea5e9',textDecoration:'underline'}}>owner@aifolio.com</a>.
      </div>
    </section>
  );
}
