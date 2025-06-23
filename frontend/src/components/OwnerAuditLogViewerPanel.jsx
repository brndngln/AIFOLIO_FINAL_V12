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
    <section aria-labelledby="audit-log-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="audit-log-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>OWNER Audit Log Viewer</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Audit log viewer" title="View and filter static audit logs. Export as JSON or CSV. OWNER only." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <div style={{marginBottom:16}}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search logs by date, action, user, or vault..."
          style={{padding:8,borderRadius:6,border:'1px solid #d1d5db',width:'100%',maxWidth:320,fontSize:15}}
        />
      </div>
      {status && <div style={{color:'#b91c1c',marginBottom:10}}>{status}</div>}
      {/* Notification for new compliance errors/manual overrides */}
      {filtered.some(l => l.status==='manual_override_needed' || l.status==='compliance_failed') && (
        <div style={{background:'#fef2f2',color:'#b91c1c',padding:10,borderRadius:6,marginBottom:10,fontWeight:600}}>
          Attention: Some vaults require manual override or failed compliance. Please review and resolve flagged issues below.
        </div>
      )}
      <div style={{marginBottom:16,display:'flex',gap:8}}>
        <button onClick={()=>handleExport('json')} style={{background:'#0ea5e9',color:'#fff',border:'none',padding:'6px 16px',borderRadius:6,fontWeight:700,cursor:'pointer'}}>Export JSON</button>
        <button onClick={()=>handleExport('csv')} style={{background:'#f3f4f6',color:'#111',border:'1px solid #d1d5db',padding:'6px 16px',borderRadius:6,fontWeight:700,cursor:'pointer'}}>Export CSV</button>
      </div>
      <div style={{maxHeight:420,overflowY:'auto',border:'1px solid #e5e7eb',borderRadius:8}}>
        <table style={{width:'100%',fontSize:15,borderCollapse:'collapse'}}>
          <thead>
            <tr style={{background:'#f1f5f9'}}>
              <th style={{padding:'8px 6px',textAlign:'left'}}>Date/Time</th>
              <th style={{padding:'8px 6px',textAlign:'left'}}>Action</th>
              <th style={{padding:'8px 6px',textAlign:'left'}}>User</th>
              <th style={{padding:'8px 6px',textAlign:'left'}}>Vault</th>
              <th style={{padding:'8px 6px',textAlign:'left'}}>Status</th>
              <th style={{padding:'8px 6px',textAlign:'left'}}>Error/Message</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} style={{padding:18,textAlign:'center',color:'#888'}}>No logs found.</td></tr>
            ) : (
              filtered.map((l,i) => (
                <tr key={i} style={{background:l.status==='manual_override_needed' ? '#fff7ed' : l.status==='compliance_failed' ? '#fef2f2' : '#fff',color:l.status==='manual_override_needed' ? '#b45309' : l.status==='compliance_failed' ? '#b91c1c' : '#222'}}>
                  <td style={{padding:'6px 4px'}}>{l.date||l.timestamp||''}</td>
                  <td style={{padding:'6px 4px'}}>{l.action||''}</td>
                  <td style={{padding:'6px 4px'}}>{l.user||''}</td>
                  <td style={{padding:'6px 4px'}}>{l.vault||''}</td>
                  <td style={{padding:'6px 4px',fontWeight:700}}>{l.status||''}</td>
                  <td style={{padding:'6px 4px',maxWidth:220,overflow:'hidden',textOverflow:'ellipsis'}}>{l.error||l.message||''}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
