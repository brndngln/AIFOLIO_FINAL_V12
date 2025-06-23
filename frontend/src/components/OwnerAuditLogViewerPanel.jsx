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

  useEffect(() => {
    fetch("/analytics/audit_log.json")
      .then(r => r.json())
      .then(data => {
        setLogs(Array.isArray(data) ? data : []);
        setFiltered(Array.isArray(data) ? data : []);
      })
      .catch(() => setStatus("Could not load audit log."));
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

  return (
    <section aria-labelledby="audit-log-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="audit-log-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>OWNER Audit Log Viewer</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Audit log viewer" title="View and filter static audit logs. Export as JSON or CSV. OWNER only." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <div style={{marginBottom:16}}>
        <input
          type="text"
          placeholder="Search by date, action, or user..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          aria-label="Search audit logs"
          style={{padding:8,borderRadius:6,border:'1px solid #e5e7eb',width:'100%',maxWidth:320}}
        />
      </div>
      <div style={{maxHeight:220,overflowY:'auto',marginBottom:12,border:'1px solid #e5e7eb',borderRadius:8,background:'#fff'}}>
        <table style={{width:'100%',fontSize:14,borderCollapse:'collapse'}} aria-label="Audit log table">
          <thead>
            <tr style={{background:'#f1f5f9'}}>
              <th style={{padding:8,textAlign:'left',color:'#0ea5e9'}}>Date</th>
              <th style={{padding:8,textAlign:'left',color:'#0ea5e9'}}>Action</th>
              <th style={{padding:8,textAlign:'left',color:'#0ea5e9'}}>User</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={3} style={{padding:12,color:'#64748b'}}>No audit log entries found.</td></tr>
            ) : filtered.map((l, i) => (
              <tr key={i}>
                <td style={{padding:8,borderBottom:'1px solid #e5e7eb'}}>{l.date || ''}</td>
                <td style={{padding:8,borderBottom:'1px solid #e5e7eb'}}>{l.action || ''}</td>
                <td style={{padding:8,borderBottom:'1px solid #e5e7eb'}}>{l.user || ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{display:'flex',gap:16,marginBottom:8}}>
        <button onClick={()=>handleExport('json')} style={{background:'#0ea5e9',color:'#fff',border:'none',borderRadius:6,padding:'8px 16px',fontWeight:700,cursor:'pointer'}}>Export as JSON</button>
        <button onClick={()=>handleExport('csv')} style={{background:'#0ea5e9',color:'#fff',border:'none',borderRadius:6,padding:'8px 16px',fontWeight:700,cursor:'pointer'}}>Export as CSV</button>
      </div>
      <div style={{color:'#64748b',fontSize:13}}>{status}</div>
      <div style={{marginTop:10,color:'#64748b',fontSize:13}}>
        <b>OWNER CONTROLLED:</b> Audit log is static, read-only, and exportable by OWNER only.
      </div>
    </section>
  );
}
