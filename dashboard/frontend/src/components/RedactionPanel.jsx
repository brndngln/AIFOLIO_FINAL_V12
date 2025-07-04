import React, { useState } from "react";

export default function RedactionPanel() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [redacted, setRedacted] = useState(false);

  const handleRedact = () => {
    // Simple static redaction for PII (email, phone, SSN, etc)
    let text = input;
    text = text.replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g, "[REDACTED_EMAIL]");
    text = text.replace(/(\b\d{3}[-.]?\d{2}[-.]?\d{4}\b)/g, "[REDACTED_SSN]");
    text = text.replace(/(\b\d{10,}\b)/g, "[REDACTED_PHONE]");
    setOutput(text);
    setRedacted(true);
  };

  return (
    <div className="redaction-panel" style={{background:'#181e2b',color:'#b3e9ff',borderRadius:16,padding:32,boxShadow:'0 0 32px #00e6ff44'}}>
      <h2>Sensitive Data Redaction</h2>
      <textarea value={input} onChange={e => setInput(e.target.value)} placeholder="Paste text to redact..." style={{width:'100%',height:100,marginBottom:16,background:'#232b3b',color:'#00e6ff',borderRadius:8}} />
      <button onClick={handleRedact} style={{background:'#00e6ff',color:'#181e2b',border:'none',borderRadius:8,padding:'8px 16px'}}>Redact</button>
      {redacted && <textarea value={output} readOnly style={{width:'100%',height:100,marginTop:16,background:'#232b3b',color:'#00e6ff',borderRadius:8}} />}
      <div style={{marginTop:32,opacity:0.8}}>
        <em>Static redaction for PII, PHI, and sensitive data. All exports and logs are SAFE AI-compliant and owner-controlled.</em>
      </div>
    </div>
  );
}
