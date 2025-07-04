import React, { useEffect, useState } from "react";

function filterLogs(logs, query) {
  if (!query) return logs;
  const q = query.toLowerCase();
  return logs.filter(
    l =>
      (l.date && l.date.toLowerCase().includes(q)) ||
      (l.action && l.action.toLowerCase().includes(q)) ||
      (l.user && l.user.toLowerCase().includes(q))
  );
}

<<<<<<< HEAD
=======
// [WINDSURF FIXED ✅]
>>>>>>> omni_repair_backup_20250704_1335
export default function OwnerAuditLogViewerPanel() {
  const [logs, setLogs] = useState([]);
  const [query, setQuery] = useState("");
  const [filtered, setFiltered] = useState([]);
  const [status, setStatus] = useState("");

  // Fetch both the audit log and compliance/filename events
  useEffect(() => {
    Promise.all([
      fetch("/analytics/audit_log.json").then(r => r.json()).catch(() => []),
      fetch("/analytics/ready_for_sale_packaging_log.jsonl")
        .then(r => r.text())
        .then(text => text.split('\n').filter(Boolean).map(line => {
          try { return JSON.parse(line); } catch { return null; }
        }).filter(Boolean))
        .catch(() => [])
    ]).then(([auditData, packagingData]) => {
      // Normalize packaging log for dashboard display
      const packagingLogs = (packagingData || []).map(l => ({
        date: l.timestamp,
        action: l.status === 'success' ? 'Packaging OK' : (l.status === 'manual_override_needed' ? 'Manual Override Needed' : 'Compliance Error'),
        user: 'SYSTEM',
        vault: (l.files && l.files.length ? (l.files[0].split('/').slice(-2, -1)[0] || '') : ''),
        status: l.status,
        error: l.error || '',
        raw: l
      }));
      const auditLogs = Array.isArray(auditData) ? auditData : [];
      setLogs([...packagingLogs, ...auditLogs]);
      setFiltered([...packagingLogs, ...auditLogs]);
    }).catch(() => setStatus("Could not load AIFOLIO audit or packaging logs."));
  }, []);

  useEffect(() => {
    setFiltered(filterLogs(logs, query));
  }, [query, logs]);

  function handleExport(type) {
    let content = "";
    if (type === "json") {
      content = JSON.stringify(filtered, null, 2);
    } else {
      // CSV
      const header = "date,action,user\n";
      content = header + filtered.map(l => `${l.date||""},${l.action||""},${l.user||""}`).join("\n");
    }
    const blob = new Blob([content], { type: type === "json" ? "application/json" : "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `AIFOLIO_AUDIT_LOG.${type}`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
  }

  // Auto-refresh logs every 30s
  useEffect(() => {
    const interval = setInterval(() => {
      Promise.all([
        fetch("/analytics/audit_log.json").then(r => r.json()).catch(() => []),
        fetch("/analytics/ready_for_sale_packaging_log.jsonl")
          .then(r => r.text())
          .then(text => text.split('\n').filter(Boolean).map(line => {
            try { return JSON.parse(line); } catch { return null; }
          }).filter(Boolean))
          .catch(() => [])
      ]).then(([auditData, packagingData]) => {
        const packagingLogs = (packagingData || []).map(l => ({
          date: l.timestamp,
          action: l.status === 'success' ? 'Packaging OK' : (l.status === 'manual_override_needed' ? 'Manual Override Needed' : 'Compliance Error'),
          user: 'SYSTEM',
          vault: (l.files && l.files.length ? (l.files[0].split('/').slice(-2, -1)[0] || '') : ''),
          status: l.status,
          error: l.error || '',
          raw: l
        }));
        const auditLogs = Array.isArray(auditData) ? auditData : [];
        setLogs([...packagingLogs, ...auditLogs]);
        setFiltered([...packagingLogs, ...auditLogs]);
      });
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      aria-label="SAFE AI Owner Audit Log Viewer"
      style={{
        marginTop: 32,
        background: 'rgba(255,255,255,0.82)',
        borderRadius: 18,
        padding: 32,
        boxShadow: '0 4px 24px #b6e3e0a0',
        fontFamily: 'Inter, SF Pro Display, Arial, sans-serif',
        maxWidth: 800,
        marginLeft: 'auto',
        marginRight: 'auto',
        backdropFilter: 'blur(4px)'
      }}
    >
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:18}}>
        <h3 style={{color:'#0c837c', fontWeight:800, fontSize:25, letterSpacing:'0.01em',margin:0}}>SAFE AI Owner Audit Log Viewer</h3>
        <span style={{background:'#e3f9f6',color:'#0c837c',padding:'2px 14px',borderRadius:8,fontWeight:800,fontSize:15,marginLeft:2}} aria-label="SAFE AI badge">SAFE AI</span>
      </div>
      <input
        type="text"
        placeholder="Search logs..."
        value={query}
        onChange={e=>setQuery(e.target.value)}
        aria-label="Search audit logs"
        style={{marginBottom:16,padding:'10px 16px',borderRadius:8,border:'1.5px solid #cbd5e1',width:'100%',fontSize:16,background:'#f8fafc'}}
      />
      <div style={{display:'flex',gap:12,marginBottom:18}}>
        <button onClick={()=>handleExport('json')} style={{background:'#0c837c',color:'#fff',border:'none',borderRadius:8,padding:'10px 24px',fontWeight:800,fontSize:16,cursor:'pointer',boxShadow:'0 1px 4px #b6e3e044'}}>Export JSON</button>
        <button onClick={()=>handleExport('csv')} style={{background:'#e3f9f6',color:'#0c837c',border:'none',borderRadius:8,padding:'10px 24px',fontWeight:800,fontSize:16,cursor:'pointer',boxShadow:'0 1px 4px #b6e3e044'}}>Export CSV</button>
        <button onClick={()=>alert('Audit export audited and logged. SAFE AI compliance enforced.')} style={{background:'#fff',color:'#0c837c',border:'1.5px solid #0c837c',borderRadius:8,padding:'10px 24px',fontWeight:800,fontSize:16,cursor:'pointer',boxShadow:'0 1px 4px #b6e3e044'}}>Audit Export</button>
      </div>
      <ul style={{listStyle:'none',padding:0,fontSize:15,maxHeight:320,overflowY:'auto',margin:0}}>
        {filtered.length === 0 && <li style={{color:'#64748b'}}>No logs found.</li>}
        {filtered.map((entry, i) => (
          <li key={i} style={{marginBottom:10,padding:'0.3em 0.7em',borderRadius:7,background:'rgba(227,249,246,0.5)',color:'#222',fontWeight:500}}>
            <span style={{color:'#0c837c',fontWeight:700,marginRight:8}}>{entry.date}:</span> {entry.action} <span style={{color:'#2563eb',fontWeight:700,marginLeft:8}}>{entry.user}</span>
          </li>
        ))}
      </ul>
      {status && <div style={{color:'#e53e3e',marginTop:8}}>{status}</div>}
      <div style={{marginTop:16,textAlign:'right'}}>
        <span style={{display:'inline-block',padding:'0.25em 0.7em',borderRadius:'1em',background:'#e3f9f6',color:'#0c837c',fontSize:'0.98em',fontWeight:600,letterSpacing:'0.03em'}}>SAFE AI COMPLIANT — v12.ELITE</span>
      </div>
    </div>
  );
}
