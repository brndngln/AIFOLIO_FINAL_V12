import React, { useState } from "react";

const steps = [
  { title: "Welcome to AIFOLIO!", content: "This tour will guide you through the elite features of your business dashboard." },
  { title: "Elite Audit Dashboard", content: "Monitor SAFE AI, privacy, and security compliance in real time." },
  { title: "Prompt Marketplace", content: "Submit, review, and monetize prompt sets with owner moderation." },
  { title: "Workflow Builder", content: "Design multi-step, owner-controlled prompt workflows." },
  { title: "Export Panel", content: "Export branded, licensing-ready deliverables in multiple formats." },
  { title: "Automation Builder", content: "Connect vault events to external services with no code." },
  { title: "Billing & Partner Program", content: "Manage subscriptions, partners, and affiliate programs." },
  { title: "Leaderboard", content: "Track vault usage, exports, and community contributions." }
];

export default function OnboardingTour() {
  const [step, setStep] = useState(0);
  return (
    <div className="onboarding-tour" style={{background:'#181e2b',color:'#b3e9ff',borderRadius:16,padding:32,boxShadow:'0 0 32px #00e6ff44',maxWidth:500,margin:'0 auto'}}>
      <h2>{steps[step].title}</h2>
      <p>{steps[step].content}</p>
      <div style={{marginTop:24}}>
        <button onClick={() => setStep(s => Math.max(0, s-1))} disabled={step===0} style={{marginRight:8,background:'#232b3b',color:'#00e6ff',border:'none',borderRadius:8,padding:'8px 16px'}}>Back</button>
        <button onClick={() => setStep(s => Math.min(steps.length-1, s+1))} disabled={step===steps.length-1} style={{background:'#00e6ff',color:'#181e2b',border:'none',borderRadius:8,padding:'8px 16px'}}>Next</button>
      </div>
      <div style={{marginTop:32,opacity:0.8}}>
        <em>Elite onboarding for owner empowerment and rapid mastery.</em>
      </div>
    </div>
  );
}
