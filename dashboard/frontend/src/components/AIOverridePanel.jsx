import React, { useState } from "react";

export default function AIOverridePanel() {
  const [output, setOutput] = useState("Sample AI output: ...");
  const [approved, setApproved] = useState(false);
  const [edited, setEdited] = useState("");

  const handleApprove = () => {
    setApproved(true);
  };
  const handleEdit = () => {
    setOutput(edited);
    setApproved(false);
  };

  return (
    <div className="ai-override-panel" style={{background:'#181e2b',color:'#b3e9ff',borderRadius:16,padding:32,boxShadow:'0 0 32px #00e6ff44'}}>
      <h2>Owner AI Override Panel</h2>
      <textarea value={edited || output} onChange={e => setEdited(e.target.value)} style={{width:'100%',height:100,marginBottom:16,background:'#232b3b',color:'#00e6ff',borderRadius:8}} />
      <div>
        <button onClick={handleEdit} style={{background:'#232b3b',color:'#00e6ff',border:'none',borderRadius:8,padding:'8px 16px',marginRight:8}}>Edit</button>
        <button onClick={handleApprove} style={{background:'#00e6ff',color:'#181e2b',border:'none',borderRadius:8,padding:'8px 16px'}} disabled={approved}>{approved ? "Approved" : "Approve"}</button>
      </div>
      <div style={{marginTop:32,opacity:0.8}}>
        <em>Owner can approve, reject, or edit any AI-generated output before delivery or export. Full control, always.</em>
      </div>
    </div>
  );
}
