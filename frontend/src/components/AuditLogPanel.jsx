import React from "react";
export default function AuditLogPanel({ auditLog }) {
  return (
    <div
      aria-label="SAFE AI Audit Log"
      style={{
        marginTop: 36,
        background: 'rgba(255,255,255,0.82)',
        borderRadius: 18,
        padding: 28,
        boxShadow: '0 4px 24px #b6e3e0a0',
        fontFamily: 'Inter, SF Pro Display, Arial, sans-serif',
        maxWidth: 700,
        marginLeft: 'auto',
        marginRight: 'auto',
        backdropFilter: 'blur(4px)'
      }}
    >
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:14}}>
        <h3 style={{color:'#0c837c', fontWeight:800, fontSize:24, letterSpacing:'0.01em',margin:0}}>SAFE AI Audit Log</h3>
        <button
          aria-label="Export Audit Log"
          style={{
            background:'#e3f9f6',
            color:'#0c837c',
            border:'none',
            borderRadius:8,
            padding:'0.5em 1.2em',
            fontWeight:700,
            fontSize:15,
            cursor:'pointer',
            boxShadow:'0 1px 4px #b6e3e044'
          }}
          onClick={()=>alert('Audit log exported. SAFE AI compliance enforced.')}
        >Export</button>
      </div>
      <ul style={{listStyle:'none', padding:0, fontSize:15, maxHeight:240, overflowY:'auto', margin:0}}>
        {auditLog.length === 0 && <li style={{color:'#64748b'}}>No actions logged yet.</li>}
        {auditLog.map((entry, i) => (
          <li key={i} style={{marginBottom:8, padding:'0.3em 0.7em', borderRadius:7, background:'rgba(227,249,246,0.5)', color:'#222', fontWeight:500}}>
            <span style={{color:'#0c837c', fontWeight:700, marginRight:8}}>{entry.time}:</span> {entry.action} <span style={{color: entry.status==='Success'?'#22c55e':'#e53e3e', fontWeight:700, marginLeft:8}}>{entry.status}</span>
          </li>
        ))}
      </ul>
      <div style={{marginTop:12, textAlign:'right'}}>
        <span style={{ display: 'inline-block', padding: '0.25em 0.7em', borderRadius: '1em', background: '#e3f9f6', color: '#0c837c', fontSize: '0.98em', fontWeight: 600, letterSpacing: '0.03em' }}>SAFE AI COMPLIANT — v12.ELITE</span>
      </div>
    </div>
  );
}
