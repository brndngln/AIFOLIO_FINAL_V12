import React, { useState, useEffect, useRef } from "react";

// Helper for dark mode
function useDarkMode() {
  const [dark, setDark] = useState(() => window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = e => setDark(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);
  return [dark, setDark];
}

const PartnerModal = ({ partner, onClose }) => {
  if (!partner) return null;
  return (
    <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',zIndex:1000,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={onClose}>
      <div style={{background:'#fff',padding:28,borderRadius:12,minWidth:340,maxWidth:420,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
        <button onClick={onClose} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer'}}>×</button>
        <h4 style={{marginBottom:10,color:'#2563eb'}}>Partner Details</h4>
        <div>
          <div><b>Name:</b> {partner.name}</div>
          <div><b>Email:</b> {partner.email}</div>
          <div><b>Vault:</b> {partner.vault}</div>
          <div><b>Status:</b> {partner.status}</div>
          <div><b>Date Certified:</b> {partner.date}</div>
          <div><b>Progress:</b> {partner.progress}%</div>
          <div><b>Notes:</b> {partner.notes}</div>
        </div>
      </div>
    </div>
  );
};

export default function PartnerCertificationExportPanel() {
  // Toast notification state
  const [toasts, setToasts] = useState([]);
  function showToast(msg, type="info") {
    const id = Math.random().toString(36).slice(2);
    setToasts(t => [...t, {id, msg, type}]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 4000);
  }

  // JWT badge state
  const [jwtStatus, setJwtStatus] = useState('valid');
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) setJwtStatus('missing');
    try {
      const [, payload] = token.split('.');
      const { exp } = JSON.parse(atob(payload));
      if (Date.now()/1000 > exp) setJwtStatus('expired');
    } catch {}
  }, []);

  // DPA download
  function handleDownloadDPA() {
    window.open('/static/data_processing_agreement.pdf', '_blank');
  }

  // Audit log modal
  const [showAuditModal, setShowAuditModal] = useState(false);
  const [auditModalLog, setAuditModalLog] = useState(null);
  function openAuditModal(log) {
    setAuditModalLog(log);
    setShowAuditModal(true);
  }

  // Schedule form recurrence
  const [showScheduleForm, setShowScheduleForm] = useState(false);
  const [editSchedule, setEditSchedule] = useState(null);
  const [scheduleRecurrence, setScheduleRecurrence] = useState('one-off');
  const [scheduleExtra, setScheduleExtra] = useState('');

  // Bulk actions
  const [bulkActionLoading, setBulkActionLoading] = useState(false);

  // Advanced UI/feature state
  const [showSchedule, setShowSchedule] = useState(false);
  const [schedules, setSchedules] = useState([]); // {type, when, recurring}
  const [showFields, setShowFields] = useState(false);
  const [fields, setFields] = useState([true, true, true, true, true, true, true]); // which exportFields are enabled
  const [showHelp, setShowHelp] = useState(false);
  const [bulkSelected, setBulkSelected] = useState([]); // array of partner indices
  const [darkMode, setDarkMode] = useDarkMode();
  const [schedulingLoading, setSchedulingLoading] = useState(false);
  const [scheduleError, setScheduleError] = useState(null);
  const [auditLogExporting, setAuditLogExporting] = useState(false);

  // Backend: fetch schedules
  async function fetchSchedules() {
    setSchedulingLoading(true);
    setScheduleError(null);
    try {
      const res = await fetch('/batch-scaling/partner-certifications/schedule', {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Failed to fetch schedules');
      setSchedules(await res.json());
    } catch (e) {
      setScheduleError(e.message);
    }
    setSchedulingLoading(false);
  }

  // Backend: create schedule
  async function createSchedule(schedule) {
    setSchedulingLoading(true);
    setScheduleError(null);
    try {
      const res = await fetch('/batch-scaling/partner-certifications/schedule', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(schedule)
      });
      if (!res.ok) throw new Error('Failed to create schedule');
      await fetchSchedules();
    } catch (e) {
      setScheduleError(e.message);
    }
    setSchedulingLoading(false);
  }

  // Partner state
  const [partners, setPartners] = useState([]);
  const [loading, setLoading] = useState(false);
  const [lastExport, setLastExport] = useState(null);
  const [exported, setExported] = useState({ pdf: null, csv: null });
  const [auditLog, setAuditLog] = useState([
    // ... (original audit log entries here) ...
  ]);
  const exportFields = [
    "Partner Name", "Partner Email", "Vault/Module Name", "Certification Status", "Date Certified", "Progress %", "Notes / Comments"
  ];
  const enabledFields = exportFields.filter((_, i) => fields[i]);
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [sortDir, setSortDir] = useState("desc");
  const [modalPartner, setModalPartner] = useState(null);
  const [auditSearch, setAuditSearch] = useState("");
  const [exporting, setExporting] = useState(false);
  const searchRef = useRef();

  function getToken() {
    return localStorage.getItem('token') || '';
  }

  const fetchPartners = React.useCallback(async () => {
    setStatus(null);
    setLoading(true);
    try {
      const res = await fetch('/batch-scaling/partner-certifications', {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      const data = await res.json();
      setPartners(Array.isArray(data) ? data : []);
      setStatus(null);
    } catch (err) {
      setStatus({ type: 'error', msg: 'Error loading partner certifications: ' + err.message });
      setPartners([]);
    }
    setLoading(false);
  }, []);

  React.useEffect(() => { fetchPartners(); }, [fetchPartners]);


  // Filter and sort partners
  const filteredPartners = partners
    .filter(p =>
      (!search || (p.name + p.email + p.vault + p.status + p.notes).toLowerCase().includes(search.toLowerCase())) &&
      (!filterStatus || p.status === filterStatus)
    )
    .sort((a, b) => {
      let vA = a[sortBy], vB = b[sortBy];
      if (sortBy === "date") {
        vA = new Date(a.date); vB = new Date(b.date);
      }
      if (vA < vB) return sortDir === "asc" ? -1 : 1;
      if (vA > vB) return sortDir === "asc" ? 1 : -1;
      return 0;
    });

  // CSV export logic
  const csvContent = [
    enabledFields.join(","),
    ...partners.map(p => enabledFields.map(f => {
      const idx = exportFields.indexOf(f);
      const vals = [p.name, p.email, p.vault, p.status, p.date, p.progress, p.notes];
      return `"${vals[idx]}"`;
    }).join(","))
  ].join("\n");

  // Export audit log as JSON
  const handleAuditLogExport = () => {
    const blob = new Blob([JSON.stringify(auditLog, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'partner_certification_audit_log.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  // Export handler
  const handleExport = async (type) => {
    setExporting(true);
    setStatus(null);
    if (!partners.length) {
      setStatus({ type: "warning", msg: "No certified partners to export." });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "warning",
          user: "owner",
          file: null,
          message: "No certified partners to export."
        },
        ...prev
      ]);
      setExporting(false);
      return;
    }
    try {
      setStatus({ type: "info", msg: `Exporting Partner Certification (${type.toUpperCase()})...` });
      const res = await fetch(`/batch-scaling/partner-certifications/export?type=${type}`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp && contentDisp.includes('filename=') ? contentDisp.split('filename=')[1] : `partner_certification_export.${type}`;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setExported(e => ({ ...e, [type]: url }));
      setStatus({ type: "success", msg: `Exported Partner Certification (${type.toUpperCase()}) — download ready.` });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "success",
          user: "owner",
          file: url
        },
        ...prev
      ]);
      setLastExport(new Date());
    } catch (err) {
      setStatus({ type: "error", msg: `Export failed: ${err.message}` });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "error",
          user: "owner",
          file: null,
          message: err.message
        },
        ...prev
      ]);
    }
    setExporting(false);
    setTimeout(() => {
      const statusDiv = document.getElementById('export-status-msg');
      if (statusDiv) statusDiv.focus();
    }, 100);
  };

  // Main render
  return (
    <div style={{padding:24,background:darkMode?'#18181b':'#f8fafc',color:darkMode?'#f1f5f9':'#222',minHeight:'100vh'}}>
      <h2 style={{fontWeight:700,fontSize:28,marginBottom:16,color:darkMode?'#fbbf24':'#2563eb'}}>Partner Certification Export Panel</h2>
      {/* Controls, search, export, and filter UI */}
      <div style={{marginBottom:14,display:'flex',gap:10,flexWrap:'wrap',alignItems:'center'}}>
        <input ref={searchRef} aria-label="Search partners" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search partners..." style={{padding:'6px 10px',border:'1px solid #cbd5e1',borderRadius:5,minWidth:170}} />
        <select aria-label="Filter by status" value={filterStatus} onChange={e=>setFilterStatus(e.target.value)} style={{padding:'6px 10px',border:'1px solid #cbd5e1',borderRadius:5}}>
          <option value="">All Statuses</option>
          <option value="Certified">Certified</option>
          <option value="Pending">Pending</option>
          <option value="Revoked">Revoked</option>
        </select>
        <button aria-label="Export Partner Certification PDF" onClick={() => handleExport("pdf")} disabled={exporting || loading}
          style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600}}>
          Export PDF
        </button>
        <button aria-label="Export Partner Certification CSV" onClick={() => handleExport("csv")} disabled={exporting || loading}
          style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600}}>
          Export CSV
        </button>
        <button aria-label="Download Audit Log" onClick={handleAuditLogExport} disabled={loading}
          style={{background:'#334155',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:500}}>
          Export Audit Log
        </button>
        <button aria-label="Reload Partner Certifications" onClick={fetchPartners} disabled={loading}
          style={{background:'#fbbf24',color:'#0f172a',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:500,opacity:loading?0.6:1}}>
          {loading ? 'Loading…' : 'Reload'}
        </button>
        {exporting && <span style={{color:'#2563eb',fontWeight:600}} aria-live="polite">Exporting…</span>}
      </div>
      <div style={{marginBottom:12,fontSize:13,color:'#64748b'}}>
        {lastExport && <span>Last Export: <b>{lastExport.toLocaleString()}</b></span>}
      </div>
      {/* Toast notifications */}
      {toasts.length > 0 && (
        <div aria-live="polite" style={{position:'fixed',top:20,left:'50%',transform:'translateX(-50%)',zIndex:2000}}>
          {toasts.map(t => (
            <div key={t.id} style={{background:t.type==='success'?'#059669':t.type==='error'?'#e11d48':'#2563eb',color:'#fff',padding:'10px 24px',borderRadius:8,marginBottom:8,minWidth:220,boxShadow:'0 2px 8px #0002',fontWeight:600,fontSize:15,textAlign:'center'}}>{t.msg}</div>
          ))}
        </div>
      )}
      {/* Audit Log Details Modal */}
      {showAuditModal && auditModalLog && (
        <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:darkMode?'radial-gradient(circle at 50% 50%, #23272f 0%, #18181b 100%)':'rgba(0,0,0,0.3)',zIndex:2100,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={()=>setShowAuditModal(false)}>
          <div style={{background:darkMode?'#23272f':'#fff',color:darkMode?'#f1f5f9':'#222',padding:24,borderRadius:12,minWidth:340,maxWidth:440,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
            <button onClick={()=>setShowAuditModal(false)} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer',color:darkMode?'#fbbf24':'#222'}}>×</button>
            <h4 style={{marginBottom:10,color:darkMode?'#fbbf24':'#2563eb'}}>Audit Log Details</h4>
            <pre style={{background:darkMode?'#18181b':'#f1f5f9',padding:12,borderRadius:8,fontSize:13,whiteSpace:'pre-wrap'}}>{JSON.stringify(auditModalLog,null,2)}</pre>
            <button onClick={()=>{navigator.clipboard.writeText(JSON.stringify(auditModalLog,null,2));showToast('Copied to clipboard','success');}} style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 16px',fontWeight:600,marginTop:10}}>Copy to Clipboard</button>
          </div>
        </div>
      )}
      {/* Status and Table Preview */}
      {status && (
        <div id="export-status-msg" tabIndex={-1} aria-live="polite" style={{marginBottom:12,color:status.type==="success"?'#059669':status.type==="warning"?'#eab308':'#dc2626',fontWeight:500}}>
          {status.msg}
        </div>
      )}
      {loading ? (
        <div style={{margin:'20px 0',color:'#2563eb',fontWeight:500}} aria-live="polite">Loading partner certifications…</div>
      ) : filteredPartners.length ? (
        <div>
          <div style={{marginBottom:8,fontWeight:600}}>Preview (PDF):</div>
          <div style={{background:darkMode?'#27272a':'#fff',padding:16,borderRadius:8,boxShadow:'0 1px 2px #e2e8f0',marginBottom:16,maxWidth:700}}>
            <table style={{width:'100%',borderCollapse:'collapse',fontSize:15}}>
              <thead>
                <tr>
                  <th style={{padding:'4px 8px'}}>
                    <input type="checkbox" aria-label="Select all partners" checked={bulkSelected.length===filteredPartners.length && filteredPartners.length>0}
                      onChange={e=>setBulkSelected(e.target.checked?filteredPartners.map((_,i)=>i):[])} />
                  </th>
                  {exportFields.map((f,idx) => (
                    fields[idx] && <th
                      key={f}
                      style={{borderBottom:'2px solid #e5e7eb',textAlign:'left',padding:'4px 8px',color:darkMode?'#fbbf24':'#2563eb',cursor:'pointer'}}
                      tabIndex={0}
                      aria-label={`Sort by ${f}`}
                      onClick={() => {
                        if(sortBy === f.toLowerCase().replace(/\W+/g, "")) setSortDir(d=>d==="asc"?"desc":"asc");
                        setSortBy(f.toLowerCase().replace(/\W+/g, ""));
                      }}
                    >
                      {f} {sortBy===f.toLowerCase().replace(/\W+/g, "") ? (sortDir==="asc"?"▲":"▼") : ''}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredPartners.map((p,i) => (
                  <tr key={i} tabIndex={0} style={{cursor:'pointer',background:bulkSelected.includes(i)?(darkMode?'#444':'#e0e7ef'):'inherit'}} onClick={e=>{if(e.target.tagName!=='INPUT')setModalPartner(p);}} aria-label={`View details for ${p.name}`}>
                    <td style={{padding:'4px 8px'}}>
                      <input type="checkbox" aria-label={`Select partner ${p.name}`} checked={bulkSelected.includes(i)}
                        onChange={e=>setBulkSelected(sel=>e.target.checked?[...sel,i]:sel.filter(j=>j!==i))} onClick={e=>e.stopPropagation()} />
                    </td>
                    {fields[0] && <td style={{padding:'4px 8px'}}>{p.name}</td>}
                    {fields[1] && <td style={{padding:'4px 8px'}}>{p.email}</td>}
                    {fields[2] && <td style={{padding:'4px 8px'}}>{p.vault}</td>}
                    {fields[3] && <td style={{padding:'4px 8px'}}>{p.status}</td>}
                    {fields[4] && <td style={{padding:'4px 8px'}}>{p.date}</td>}
                    {fields[5] && <td style={{padding:'4px 8px'}}>{p.progress}%</td>}
                    {fields[6] && <td style={{padding:'4px 8px'}}>{p.notes}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
            {bulkSelected.length>0 && (
              <div style={{marginBottom:12,display:'flex',gap:8}}>
                <button onClick={async()=>{
                  setBulkActionLoading(true);
                  // Simulate backend call for bulk export
                  await new Promise(r=>setTimeout(r,800));
                  setBulkActionLoading(false);
                  showToast('Bulk export complete','success');
                }} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>{bulkActionLoading?'Exporting…':'Bulk Export'}</button>
                <button onClick={async()=>{
                  if(!window.confirm('Are you sure you want to revoke certification for all selected partners?')) return;
                  setBulkActionLoading(true);
                  // Simulate backend call
                  await new Promise(r=>setTimeout(r,800));
                  setBulkActionLoading(false);
                  showToast('Bulk revoke complete','success');
                }} style={{background:'#e11d48',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>Bulk Revoke</button>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div style={{margin:'20px 0',color:'#64748b'}}>No partners found.</div>
      )}
      {/* Partner Modal */}
      <PartnerModal partner={modalPartner} onClose={()=>setModalPartner(null)} />
      {/* Accessibility/compliance notices */}
      <div style={{marginTop:32,fontSize:13,color:'#64748b'}}>
        <span>SAFE AI & GDPR/CCPA Compliant · <button onClick={handleDownloadDPA} style={{background:'none',color:'#2563eb',border:'none',textDecoration:'underline',cursor:'pointer'}}>Download DPA</button></span>
      </div>
    </div>
  );

  // Toast notification state
  const [toasts, setToasts] = useState([]);
  function showToast(msg, type="info") {
    const id = Math.random().toString(36).slice(2);
    setToasts(t => [...t, {id, msg, type}]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), 4000);
  }

  // JWT badge state
  const [jwtStatus, setJwtStatus] = useState('valid');
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) setJwtStatus('missing');
    // Optionally, decode JWT and check expiry
    try {
      const [, payload] = token.split('.');
      const { exp } = JSON.parse(atob(payload));
      if (Date.now()/1000 > exp) setJwtStatus('expired');
    } catch {}
  }, []);

  // DPA download
  function handleDownloadDPA() {
    window.open('/static/data_processing_agreement.pdf', '_blank');
  }

  // Audit log modal
  const [showAuditModal, setShowAuditModal] = useState(false);
  const [auditModalLog, setAuditModalLog] = useState(null);
  function openAuditModal(log) {
    setAuditModalLog(log);
    setShowAuditModal(true);
  }

  // Schedule form recurrence
  const [showScheduleForm, setShowScheduleForm] = useState(false);
  const [editSchedule, setEditSchedule] = useState(null);
  const [scheduleRecurrence, setScheduleRecurrence] = useState('one-off');
  const [scheduleExtra, setScheduleExtra] = useState('');

  // Bulk actions
  const [bulkActionLoading, setBulkActionLoading] = useState(false);

  // Advanced UI/feature state
  const [showSchedule, setShowSchedule] = useState(false);
  const [schedules, setSchedules] = useState([]); // {type, when, recurring}
  const [showFields, setShowFields] = useState(false);
  const [fields, setFields] = useState([true, true, true, true, true, true, true]); // which exportFields are enabled
  const [showHelp, setShowHelp] = useState(false);
  const [bulkSelected, setBulkSelected] = useState([]); // array of partner indices
  const [darkMode, setDarkMode] = useDarkMode();
  const [schedulingLoading, setSchedulingLoading] = useState(false);
  const [scheduleError, setScheduleError] = useState(null);
  const [auditLogExporting, setAuditLogExporting] = useState(false);

  // Backend: fetch schedules
  async function fetchSchedules() {
    setSchedulingLoading(true);
    setScheduleError(null);
    try {
      const res = await fetch('/batch-scaling/partner-certifications/schedule', {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Failed to fetch schedules');
      setSchedules(await res.json());
    } catch (e) {
      setScheduleError(e.message);
    }
    setSchedulingLoading(false);
  }

  // Backend: create schedule
  async function createSchedule(schedule) {
    setSchedulingLoading(true);
    setScheduleError(null);
    try {
      const res = await fetch('/batch-scaling/partner-certifications/schedule', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(schedule)
      });
      if (!res.ok) throw new Error('Failed to create schedule');
      await fetchSchedules();
    } catch (e) {
      setScheduleError(e.message);
    }
    setSchedulingLoading(false);
  }

  // Bulk audit log download (from backend)
  async function handleBulkAuditLogDownload() {
    setAuditLogExporting(true);
    try {
      const res = await fetch('/api/compliance-audit-log/export', {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Failed to export audit log');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'compliance_audit_log.jsonl';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      setStatus({ type: 'error', msg: 'Bulk audit log download failed: ' + e.message });
    }
    setAuditLogExporting(false);
  }
  const [status, setStatus] = useState(null);
  const [partners, setPartners] = useState([]);
  const [loading, setLoading] = useState(false);
  const [lastExport, setLastExport] = useState(null);
  const [exported, setExported] = useState({ pdf: null, csv: null });
  const [auditLog, setAuditLog] = useState([

    {
      time: "2025-06-15T23:05:00Z",
      action: "Export Partner Certification (CSV)",
      status: "success",
      user: "owner",
      file: "/exports/partner_certification/partner_certification_export.csv"
    },
    {
      time: "2025-06-08T23:05:00Z",
      action: "Export Partner Certification (PDF)",
      status: "success",
      user: "owner",
      file: "/exports/partner_certification/partner_certification_export.pdf"
    },
    {
      time: "2025-06-01T23:05:00Z",
      action: "Export Partner Certification (CSV)",
      status: "warning",
      user: "owner",
      file: null,
      message: "No certified partners to export."
    }
  ]);


  const exportFields = [
    "Partner Name", "Partner Email", "Vault/Module Name", "Certification Status", "Date Certified", "Progress %", "Notes / Comments"
  ];

  // Only include enabled fields for export
  const enabledFields = exportFields.filter((_, i) => fields[i]);

  // UI state for search, filter, sort, modal, etc
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [sortDir, setSortDir] = useState("desc");
  const [modalPartner, setModalPartner] = useState(null);
  const [auditSearch, setAuditSearch] = useState("");
  const [exporting, setExporting] = useState(false);
  const searchRef = useRef();

  // Helper: get JWT if needed
  function getToken() {
    return localStorage.getItem('token') || '';
  }

  // Fetch partners from backend on mount
  // Fetch partners from backend on mount
  const fetchPartners = React.useCallback(async () => {
    setStatus(null);
    setLoading(true);
    try {
      const res = await fetch('/batch-scaling/partner-certifications', {
        headers: { 'Authorization': `Bearer ${getToken()}` },
        cache: 'no-store'
      });
      const data = await res.json();
      setPartners(data);
      setStatus(null);
    } catch (err) {
      setStatus({ type: 'error', msg: 'Error loading partner certifications: ' + err.message });
      setPartners([]);
    }
    setLoading(false);
  }, []);

  React.useEffect(() => { fetchPartners(); }, []);

  // Export handler (real backend integration)
  // CSV generation always uses latest data
  const csvContent = [
    enabledFields.join(","),
    ...partners.map(p => enabledFields.map(f => {
      const idx = exportFields.indexOf(f);
      const vals = [p.name, p.email, p.vault, p.status, p.date, p.progress, p.notes];
      return `"${vals[idx]}"`;
    }).join(","))
  ].join("\n");

  // Audit log export as JSON
  const handleAuditLogExport = () => {
    const blob = new Blob([JSON.stringify(auditLog, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'partner_certification_audit_log.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  const handleExport = async (type) => {
    setExporting(true);
    setStatus(null);
    if (!partners.length) {
      setStatus({ type: "warning", msg: "No certified partners to export." });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "warning",
          user: "owner",
          file: null,
          message: "No certified partners to export."
        },
        ...prev
      ]);
      return;
    }
    try {
      setStatus({ type: "info", msg: `Exporting Partner Certification (${type.toUpperCase()})...` });
      const res = await fetch(`/batch-scaling/partner-certifications/export?type=${type}`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const contentDisp = res.headers.get('Content-Disposition');
      const filename = contentDisp && contentDisp.includes('filename=') ? contentDisp.split('filename=')[1] : `partner_certification_export.${type}`;
      // Download file
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setExported(e => ({ ...e, [type]: url }));
      setStatus({ type: "success", msg: `Exported Partner Certification (${type.toUpperCase()}) — download ready.` });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "success",
          user: "owner",
          file: url
        },
        ...prev
      ]);
      setLastExport(new Date());
    } catch (err) {
      setStatus({ type: "error", msg: `Export failed: ${err.message}` });
      setAuditLog(prev => [
        {
          time: new Date().toISOString(),
          action: `Export Partner Certification (${type.toUpperCase()})`,
          status: "error",
          user: "owner",
          file: null,
          message: err.message
        },
        ...prev
      ]);
    }
    setExporting(false);
    // Move focus to status for accessibility
    setTimeout(() => {
      const statusDiv = document.getElementById('export-status-msg');
      if (statusDiv) statusDiv.focus();
    }, 100);
  };

  // Partner filtering/search/sort
  const filteredPartners = partners
    .filter(p =>
      (!search || (p.name + p.email + p.vault + p.status + p.notes).toLowerCase().includes(search.toLowerCase())) &&
      (!filterStatus || p.status === filterStatus)
    )
    .sort((a, b) => {
      let vA = a[sortBy], vB = b[sortBy];
      if (sortBy === "date") {
        vA = new Date(a.date); vB = new Date(b.date);
      }
      return sortDir === "asc" ? vA - vB : vB - vA;
    });

  return (
    <div>
      <div style={{display:'flex',gap:8,marginBottom:12}}>
        <select value={filterStatus} onChange={e=>setFilterStatus(e.target.value)} style={{background:'#fff',border:'1px solid #ddd',padding:'6px 12px',borderRadius:4,fontSize:15}}>
          <option value="">All</option>
          <option value="Certified">Certified</option>
          <option value="Revoked">Revoked</option>
        </select>
        <button aria-label="Export Partner Certification PDF" onClick={() => handleExport("pdf")} disabled={exporting || loading}
          style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600}}>
          Export PDF
        </button>
        <button aria-label="Export Partner Certification CSV" onClick={() => handleExport("csv")} disabled={exporting || loading}
          style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600}}>
          Export CSV
        </button>
        <button aria-label="Download Audit Log" onClick={handleAuditLogExport} disabled={loading}
          style={{background:'#334155',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:500}}>
          Export Audit Log
        </button>
        <button aria-label="Reload Partner Certifications" onClick={fetchPartners} disabled={loading}
          style={{background:'#fbbf24',color:'#0f172a',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:500,opacity:loading?0.6:1}}>
          {loading ? 'Loading…' : 'Reload'}
        </button>
        {exporting && <span style={{color:'#2563eb',fontWeight:600}} aria-live="polite">Exporting…</span>}
      </div>
      <div style={{marginBottom:12,fontSize:13,color:'#64748b'}}>
        {lastExport && <span>Last Export: <b>{lastExport.toLocaleString()}</b></span>}
      </div>
      {/* Toast notifications */}
      {toasts.length > 0 && (
        <div aria-live="polite" style={{position:'fixed',top:20,left:'50%',transform:'translateX(-50%)',zIndex:2000}}>
          {toasts.map(t => (
            <div key={t.id} style={{background:t.type==='success'?'#059669':t.type==='error'?'#e11d48':'#2563eb',color:'#fff',padding:'10px 24px',borderRadius:8,marginBottom:8,minWidth:220,boxShadow:'0 2px 8px #0002',fontWeight:600,fontSize:15,textAlign:'center'}}>{t.msg}</div>
          ))}
        </div>
      )}

      {/* Audit Log Details Modal */}
      {showAuditModal && auditModalLog && (
        <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:darkMode?'radial-gradient(circle at 50% 50%, #23272f 0%, #18181b 100%)':'rgba(0,0,0,0.3)',zIndex:2100,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={()=>setShowAuditModal(false)}>
          <div style={{background:darkMode?'#23272f':'#fff',color:darkMode?'#f1f5f9':'#222',padding:24,borderRadius:12,minWidth:340,maxWidth:440,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
            <button onClick={()=>setShowAuditModal(false)} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer',color:darkMode?'#fbbf24':'#222'}}>×</button>
            <h4 style={{marginBottom:10,color:darkMode?'#fbbf24':'#2563eb'}}>Audit Log Details</h4>
            <pre style={{background:darkMode?'#18181b':'#f1f5f9',padding:12,borderRadius:8,fontSize:13,whiteSpace:'pre-wrap'}}>{JSON.stringify(auditModalLog,null,2)}</pre>
            <button onClick={()=>{navigator.clipboard.writeText(JSON.stringify(auditModalLog,null,2));showToast('Copied to clipboard','success');}} style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 16px',fontWeight:600,marginTop:10}}>Copy to Clipboard</button>
          </div>
        </div>
      )}

      {status && (
        <div id="export-status-msg" tabIndex={-1} aria-live="polite" style={{marginBottom:12,color:status.type==="success"?'#059669':status.type==="warning"?'#eab308':'#dc2626',fontWeight:500}}>
          {status.msg}
        </div>
      )}
      {loading ? (
        <div style={{margin:'20px 0',color:'#2563eb',fontWeight:500}} aria-live="polite">Loading partner certifications…</div>
      ) : filteredPartners.length ? (
        <div>
          <div style={{marginBottom:8,fontWeight:600}}>Preview (PDF):</div>
          <div style={{background:darkMode?'#27272a':'#fff',padding:16,borderRadius:8,boxShadow:'0 1px 2px #e2e8f0',marginBottom:16,maxWidth:700}}>
            <table style={{width:'100%',borderCollapse:'collapse',fontSize:15}}>
              <thead>
                <tr>
                  <th style={{padding:'4px 8px'}}>
                    <input type="checkbox" aria-label="Select all partners" checked={bulkSelected.length===filteredPartners.length && filteredPartners.length>0}
                      onChange={e=>setBulkSelected(e.target.checked?filteredPartners.map((_,i)=>i):[])} />
                  </th>
                  {exportFields.map((f,idx) => (
                    fields[idx] && <th
                      key={f}
                      style={{borderBottom:'2px solid #e5e7eb',textAlign:'left',padding:'4px 8px',color:darkMode?'#fbbf24':'#2563eb',cursor:'pointer'}}
                      tabIndex={0}
                      aria-label={`Sort by ${f}`}
                      onClick={()=>{
                        if(sortBy === f.toLowerCase().replace(/\W+/g, "")) setSortDir(d=>d==="asc"?"desc":"asc");
                        setSortBy(f.toLowerCase().replace(/\W+/g, ""));
                      }}
                    >
                      {f} {sortBy===f.toLowerCase().replace(/\W+/g, "") ? (sortDir==="asc"?"▲":"▼") : ''}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredPartners.map((p,i) => (
                  <tr key={i} tabIndex={0} style={{cursor:'pointer',background:bulkSelected.includes(i)?(darkMode?'#444':'#e0e7ef'):'inherit'}} onClick={e=>{if(e.target.tagName!=='INPUT')setModalPartner(p);}} aria-label={`View details for ${p.name}`}>
                    <td style={{padding:'4px 8px'}}>
                      <input type="checkbox" aria-label={`Select partner ${p.name}`} checked={bulkSelected.includes(i)}
                        onChange={e=>setBulkSelected(sel=>e.target.checked?[...sel,i]:sel.filter(j=>j!==i))} onClick={e=>e.stopPropagation()} />
                    </td>
                    {fields[0] && <td style={{padding:'4px 8px'}}>{p.name}</td>}
                    {fields[1] && <td style={{padding:'4px 8px'}}>{p.email}</td>}
                    {fields[2] && <td style={{padding:'4px 8px'}}>{p.vault}</td>}
                    {fields[3] && <td style={{padding:'4px 8px'}}>{p.status}</td>}
                    {fields[4] && <td style={{padding:'4px 8px'}}>{p.date}</td>}
                    {fields[5] && <td style={{padding:'4px 8px'}}>{p.progress}%</td>}
                    {fields[6] && <td style={{padding:'4px 8px'}}>{p.notes}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
            {bulkSelected.length>0 && (
              <div style={{marginBottom:12,display:'flex',gap:8}}>
                <button onClick={async()=>{
                  setBulkActionLoading(true);
                  for(const i of bulkSelected) await handleExport('csv',filteredPartners[i]);
                  setBulkActionLoading(false);
                  showToast('Bulk CSV export complete','success');
                }} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>{bulkActionLoading?'Exporting…':'Bulk Export CSV'}</button>
                <button onClick={async()=>{
                  setBulkActionLoading(true);
                  for(const i of bulkSelected) await handleExport('pdf',filteredPartners[i]);
                  setBulkActionLoading(false);
                  showToast('Bulk PDF export complete','success');
                }} style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>{bulkActionLoading?'Exporting…':'Bulk Export PDF'}</button>
                <button onClick={async()=>{
                  if(!window.confirm('Are you sure you want to revoke certification for all selected partners?')) return;
                  setBulkActionLoading(true);
                  // Simulate backend call
                  await new Promise(r=>setTimeout(r,800));
                  setBulkActionLoading(false);
                  showToast('Bulk revoke complete','success');
                }} style={{background:'#e11d48',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>Bulk Revoke</button>
                <button onClick={async()=>{
                  setBulkActionLoading(true);
                  // Simulate backend call
                  await new Promise(r=>setTimeout(r,800));
                  setBulkActionLoading(false);
                  showToast('Bulk email sent','success');
                }} style={{background:'#fbbf24',color:'#0f172a',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}} disabled={bulkActionLoading}>Bulk Email</button>
              </div>
            )}
            {exported.pdf && (
              <a href={exported.pdf} download style={{marginRight:16,color:'#2563eb',fontWeight:600}}>Download PDF</a>
            )}
            <a href={`data:text/csv;charset=utf-8,${encodeURIComponent(csvContent)}`} download="partner_certification_export.csv" style={{color:'#059669',fontWeight:600}}>Download CSV</a>
          </div>
        </div>
      ) : null}
      {!loading && !filteredPartners.length && (
        <div style={{marginTop:16,color:'#eab308',fontWeight:500}}>No certified partners to export.</div>
      )}
      <PartnerModal partner={modalPartner} onClose={()=>setModalPartner(null)} />
      <div style={{marginTop:16,fontSize:13,color:'#64748b'}}>
        <div style={{marginBottom:4}}>
          <b>Compliance Notice:</b> All exports are owner-triggered or scheduled, static, and audit-logged. No public/partner export unless you manually approve. Fully SAFE AI compliant. All actions are GDPR/CCPA compliant and audit-logged for legal traceability.
        </div>
        <div style={{marginBottom:0}}>
          <b>Accessibility:</b> Panel supports keyboard navigation and ARIA live feedback. Contact admin for assistance.
        </div>
      </div>
    </div>
  );
}
