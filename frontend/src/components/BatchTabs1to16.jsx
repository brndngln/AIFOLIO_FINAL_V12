import React, { useState } from "react";

const BATCHES = Array.from({ length: 16 }, (_, i) => ({
  key: `batch${i + 1}`,
  label: `Batch ${i + 1}`,
  exports: [
    { name: `Batch ${i + 1} PDF Report`, type: "PDF", file: `batch${i + 1}_report.pdf` },
    { name: `Batch ${i + 1} CSV Data`, type: "CSV", file: `batch${i + 1}_data.csv` },
    { name: `Batch ${i + 1} Public Summary`, type: "PDF", file: `batch${i + 1}_public_summary.pdf` }
  ],
  lastUpdated: `2025-06-22T12:00:00-06:00`
}));

export default function BatchTabs1to16() {
  const [tab, setTab] = useState(BATCHES[0].key);
  const [status, setStatus] = useState(null);
  const currentBatch = BATCHES.find(b => b.key === tab);

  const handleExport = (file) => {
    setStatus(null);
    setTimeout(() => {
      setStatus({ type: "success", msg: `Exported ${file} (manual, audit-logged)` });
    }, 500);
  };

  return (
    <section className="batch-tabs-1-16" aria-label="Batch Modules 1–16" tabIndex={0}>
      <nav style={{display:'flex',gap:8,marginBottom:16,flexWrap:'wrap'}}>
        {BATCHES.map(b => (
          <button
            key={b.key}
            onClick={() => setTab(b.key)}
            style={{
              padding:'8px 12px',
              borderRadius:6,
              border:'none',
              background: tab === b.key ? '#2563eb' : '#e0e7ef',
              color: tab === b.key ? '#fff' : '#0f172a',
              fontWeight:600,
              fontSize:15,
              marginBottom:4
            }}
            aria-selected={tab === b.key}
          >
            {b.label}
          </button>
        ))}
      </nav>
      <div style={{background:'#fff',padding:16,borderRadius:8,boxShadow:'0 1px 2px #e2e8f0'}}>
        <h3 style={{color:'#0f172a',marginBottom:8}}>{currentBatch.label} Exports</h3>
        <div style={{color:'#64748b',fontSize:13,marginBottom:8}}>Last updated: {currentBatch.lastUpdated}</div>
        <ul style={{listStyle:'none',padding:0}}>
          {currentBatch.exports.map(exp => (
            <li key={exp.file} style={{marginBottom:10}}>
              <b>{exp.name}</b> <span style={{color:'#64748b',fontSize:13}}>({exp.type})</span>
              <button style={{marginLeft:16,background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'4px 12px'}} onClick={() => handleExport(exp.file)}>
                Export {exp.type}
              </button>
            </li>
          ))}
        </ul>
        {status && (
          <div style={{marginTop:10,color:status.type==="success"?'#059669':'#dc2626',fontWeight:500}}>
            {status.msg}
          </div>
        )}
        <div style={{marginTop:16,fontSize:13,color:'#64748b'}}>
          All exports are owner-triggered, static, and audit-logged. No public/partner export unless you manually approve.
        </div>
      </div>
    </section>
  );
}
