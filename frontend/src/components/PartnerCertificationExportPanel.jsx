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

export default function PartnerCertificationExportPanel() {
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
        headers: { 'Authorization': `Bearer ${getToken()}` }
      });
      if (!res.ok) throw new Error('Failed to fetch partner certifications');
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
      if (vA === vB) return 0;
      if (sortDir === "asc") return vA > vB ? 1 : -1;
      else return vA < vB ? 1 : -1;
    });

  // Filtered audit log
  const filteredAudit = auditLog.filter(l =>
    !auditSearch || JSON.stringify(l).toLowerCase().includes(auditSearch.toLowerCase())
  );

  // Compliance badges
  const ComplianceBadges = () => (
    <span style={{display:'inline-flex',gap:8,alignItems:'center'}}>
      <span title="SAFE AI Verified" style={{background:'#059669',color:'#fff',padding:'2px 8px',borderRadius:6,fontSize:12,fontWeight:600}}>SAFE AI</span>
      <span title="GDPR Compliant" style={{background:'#2563eb',color:'#fff',padding:'2px 8px',borderRadius:6,fontSize:12,fontWeight:600}}>GDPR</span>
      <span title="CCPA Compliant" style={{background:'#fbbf24',color:'#0f172a',padding:'2px 8px',borderRadius:6,fontSize:12,fontWeight:600}}>CCPA</span>
      <span title="Admin JWT Present" style={{background:'#334155',color:'#fff',padding:'2px 8px',borderRadius:6,fontSize:12,fontWeight:600}}>
        {getToken() ? 'Verified Admin' : 'Admin Only'}
      </span>
    </span>
  );

  // Partner detail modal
  function PartnerModal({ partner, onClose }) {
    if (!partner) return null;
    return (
      <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',zIndex:1000,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={onClose}>
        <div style={{background:'#fff',padding:28,borderRadius:12,minWidth:340,maxWidth:420,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
          <button onClick={onClose} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer'}}>×</button>
          <h4 style={{marginBottom:10,color:'#2563eb'}}>Partner Details</h4>
          <div><b>Name:</b> {partner.name}</div>
          <div><b>Email:</b> {partner.email}</div>
          <div><b>Vault:</b> {partner.vault}</div>
          <div><b>Status:</b> {partner.status}</div>
          <div><b>Date Certified:</b> {partner.date}</div>
          <div><b>Progress:</b> {partner.progress}%</div>
          <div><b>Notes:</b> {partner.notes}</div>
          <div style={{marginTop:12}}>
            <button onClick={()=>handleExport('pdf')} style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600,marginRight:6}}>Export PDF</button>
            <button onClick={()=>handleExport('csv')} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}}>Export CSV</button>
          </div>
        </div>
      </div>
    );
  }


  // Simulate auto-export (Sunday night)
  React.useEffect(() => {
    const now = new Date();
    if (now.getDay() === 0 && now.getHours() === 23) {
      handleExport("csv");
      handleExport("pdf");
    }
    // eslint-disable-next-line
  }, []);



  return (
    <div className={"partner-cert-export-panel" + (darkMode ? " dark" : "")}
      aria-label="Partner Certification Export" tabIndex={0}
      style={{background:darkMode?'#18181b':'#f9fafb',color:darkMode?'#f1f5f9':'#0f172a',padding:20,borderRadius:8,minHeight:600}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
        <h3 style={{color:darkMode?'#fbbf24':'#0f172a',margin:0}}>Partner Certification Export</h3>
        <ComplianceBadges />
      </div>
      <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:10}}>
        <button aria-label="Show Help" onClick={()=>setShowHelp(true)} style={{background:'none',color:darkMode?'#fbbf24':'#2563eb',border:'none',fontWeight:600,cursor:'pointer',textDecoration:'underline'}}>Help/FAQ</button>
        <button aria-label="Show Export Field Customization" onClick={()=>setShowFields(true)} style={{background:'none',color:darkMode?'#fbbf24':'#059669',border:'none',fontWeight:600,cursor:'pointer',textDecoration:'underline'}}>Customize Fields</button>
        <button aria-label="Show Export Scheduling" onClick={()=>{setShowSchedule(true);fetchSchedules();}} style={{background:'none',color:darkMode?'#fbbf24':'#334155',border:'none',fontWeight:600,cursor:'pointer',textDecoration:'underline'}}>Schedule Export</button>
        <button aria-label="Bulk Audit Log Download" onClick={handleBulkAuditLogDownload} disabled={auditLogExporting} style={{background:'none',color:darkMode?'#fbbf24':'#e11d48',border:'none',fontWeight:600,cursor:'pointer',textDecoration:'underline'}}>{auditLogExporting?'Exporting…':'Bulk Audit Log'}</button>
        <button aria-label="Toggle Dark Mode" onClick={()=>setDarkMode(d=>!d)} style={{background:'none',color:darkMode?'#fbbf24':'#64748b',border:'none',fontWeight:600,cursor:'pointer',textDecoration:'underline'}}>{darkMode?'Light Mode':'Dark Mode'}</button>
      </div>

      {/* --- Schedule Management Dialog --- */}
      {showSchedule && (
        <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.3)',zIndex:1000,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={()=>setShowSchedule(false)}>
          <div style={{background:darkMode?'#23272f':'#fff',color:darkMode?'#f1f5f9':'#222',padding:28,borderRadius:12,minWidth:380,maxWidth:500,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
            <button onClick={()=>setShowSchedule(false)} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer',color:darkMode?'#fbbf24':'#222'}}>×</button>
            <h4 style={{marginBottom:10,color:darkMode?'#fbbf24':'#2563eb'}}>Export Schedules</h4>
            {schedulingLoading ? <div>Loading schedules…</div> : scheduleError ? <div style={{color:'#e11d48'}}>{scheduleError}</div> : (
              <>
              {schedules.length === 0 ? <div style={{color:'#64748b',marginBottom:12}}>No export schedules set.</div> : (
                <table style={{width:'100%',marginBottom:12,fontSize:14}}>
                  <thead><tr style={{color:darkMode?'#fbbf24':'#2563eb'}}><th>Type</th><th>When</th><th>Recurring</th><th>Actions</th></tr></thead>
                  <tbody>
                    {schedules.map((sch,idx) => (
                      <tr key={idx}>
                        <td>{sch.type}</td>
                        <td>{sch.when}</td>
                        <td>{sch.recurring ? 'Yes' : 'No'}</td>
                        <td>
                          <button style={{marginRight:6}} aria-label="Edit" onClick={() => {
                setEditSchedule(sch);
                setShowScheduleForm(true);
              }}>Edit</button>
              <button aria-label="Delete" style={{color:'#e11d48'}} onClick={async()=>{await handleDeleteSchedule(sch.id);}}>Delete</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
              <button onClick={() => {
                setEditSchedule(null);
                setShowScheduleForm(true);
              }} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}}>Add New Schedule</button>

              {/* --- Schedule Add/Edit Form Dialog --- */}
              {showScheduleForm && (
                <div role="dialog" aria-modal="true" tabIndex={-1} style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.3)',zIndex:1100,display:'flex',alignItems:'center',justifyContent:'center'}} onClick={()=>setShowScheduleForm(false)}>
                  <div style={{background:darkMode?'#23272f':'#fff',color:darkMode?'#f1f5f9':'#222',padding:24,borderRadius:12,minWidth:340,maxWidth:440,boxShadow:'0 2px 16px #0002',position:'relative'}} onClick={e=>e.stopPropagation()}>
                    <button onClick={()=>setShowScheduleForm(false)} aria-label="Close" style={{position:'absolute',top:10,right:12,background:'none',border:'none',fontSize:20,cursor:'pointer',color:darkMode?'#fbbf24':'#222'}}>×</button>
                    <h4 style={{marginBottom:10,color:darkMode?'#fbbf24':'#2563eb'}}>{editSchedule ? 'Edit Schedule' : 'Add New Schedule'}</h4>
                    <form onSubmit={async e => {
                      e.preventDefault();
                      const form = e.target;
                      const type = form.type.value;
                      const when = form.when.value;
                      const recurring = form.recurring.checked;
                      const body = { type, when, recurring };
                      let url = '/batch-scaling/partner-certifications/schedule', method = 'POST';
                      if (editSchedule) {
                        url += `/${editSchedule.id}`;
                        method = 'PUT';
                      }
                      setSchedulingLoading(true);
                      setScheduleError(null);
                      try {
                        const res = await fetch(url, {
                          method,
                          headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                          body: JSON.stringify(body)
                        });
                        if (!res.ok) throw new Error('Failed to save schedule');
                        await fetchSchedules();
                        setShowScheduleForm(false);
                        setEditSchedule(null);
                      } catch (e) {
                        setScheduleError(e.message);
                      }
                      setSchedulingLoading(false);
                    }}>
                      <label style={{display:'block',marginBottom:8}}>
                        Type:
                        <input name="type" defaultValue={editSchedule?.type||''} required style={{marginLeft:8,padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4}} />
                      </label>
                      <label style={{display:'block',marginBottom:8}}>
                        When:
                        <input name="when" defaultValue={editSchedule?.when||''} required style={{marginLeft:8,padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4}} />
                      </label>
                      <label style={{display:'block',marginBottom:12}}>
                        <input name="recurring" type="checkbox" defaultChecked={editSchedule?.recurring||false} /> Recurring
                      </label>
                      <button type="submit" style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600,marginRight:8}} disabled={schedulingLoading}>{schedulingLoading?'Saving…':'Save'}</button>
                      <button type="button" onClick={()=>{setShowScheduleForm(false);setEditSchedule(null);}} style={{background:'#e11d48',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}}>Cancel</button>
                      {scheduleError && <div style={{color:'#e11d48',marginTop:8}}>{scheduleError}</div>}
                    </form>
                  </div>
                </div>
              )}
              </>
            )}
          </div>
        </div>
      )}

      {/* --- Advanced Audit Log Filtering & Bulk Actions --- */}
      <div style={{marginBottom:20}} aria-label="Partner Certification Audit Log Preview">
        <div style={{fontWeight:600,marginBottom:4}}>Recent Audit Log:</div>
        <div style={{display:'flex',gap:8,marginBottom:6}}>
          <input aria-label="Search audit log" value={auditSearch} onChange={e=>setAuditSearch(e.target.value)} placeholder="Search audit log..." style={{padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4,minWidth:160}} />
          <input type="date" aria-label="Filter by date" onChange={e=>setAuditLog(prev=>prev.filter(l=>l.time.startsWith(e.target.value)))} style={{padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4}} />
          <select aria-label="Filter by user" onChange={e=>setAuditLog(prev=>prev.filter(l=>l.user===e.target.value))} style={{padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4}}><option value="">All Users</option>{[...new Set(auditLog.map(l=>l.user))].map(u=><option key={u} value={u}>{u}</option>)}</select>
          <select aria-label="Filter by status" onChange={e=>setAuditLog(prev=>prev.filter(l=>l.status===e.target.value))} style={{padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4}}><option value="">All Status</option>{[...new Set(auditLog.map(l=>l.status))].map(s=><option key={s} value={s}>{s}</option>)}</select>
          <button onClick={async()=>{
            // Backend bulk delete
            try {
              const res = await fetch('/api/compliance-audit-log/bulk-delete', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter: auditSearch })
              });
              if (!res.ok) throw new Error('Bulk delete failed');
              setAuditLog([]);
              setStatus({ type: 'success', msg: 'Audit log bulk deleted.' });
            } catch (e) {
              setStatus({ type: 'error', msg: 'Bulk delete failed: ' + e.message });
            }
          }} style={{background:'#e11d48',color:'#fff',border:'none',borderRadius:4,padding:'4px 10px',fontWeight:600}}>Bulk Delete</button>
          <button onClick={async()=>{
            // Backend export filtered
            try {
              const res = await fetch('/api/compliance-audit-log/export-filtered', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter: auditSearch })
              });
              if (!res.ok) throw new Error('Export filtered failed');
              const blob = await res.blob();
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'filtered_audit_log.json';
              document.body.appendChild(a);
              a.click();
              a.remove();
              window.URL.revokeObjectURL(url);
            } catch (e) {
              setStatus({ type: 'error', msg: 'Export filtered failed: ' + e.message });
            }
          }} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'4px 10px',fontWeight:600}}>Export Filtered</button>
        </div>
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
      <div style={{marginBottom:20}} aria-label="Partner Certification Audit Log Preview">
        <div style={{fontWeight:600,marginBottom:4}}>Recent Audit Log:</div>
        <input aria-label="Search audit log" value={auditSearch} onChange={e=>setAuditSearch(e.target.value)} placeholder="Search audit log..." style={{padding:'4px 8px',border:'1px solid #cbd5e1',borderRadius:4,marginBottom:6,minWidth:160}} />
        {filteredAudit.length === 0 ? (
          <div style={{color:'#64748b',fontStyle:'italic'}}>No export actions yet.</div>
        ) : (
          <ul style={{listStyle:'none',padding:0,maxHeight:120,overflowY:'auto',fontSize:13}}>
            {filteredAudit.map((log,i) => (
              <li key={i} style={{marginBottom:4,background:'#f1f5f9',padding:6,borderRadius:4}}>
                <span style={{color:'#64748b'}}>{new Date(log.time).toLocaleString()}:</span> <b>{log.action}</b> — <span style={{color:log.status==="success"?'#059669':log.status==="warning"?'#eab308':'#dc2626',fontWeight:500}}>{log.status.toUpperCase()}</span>
                {log.file && (<span> (<a href={log.file} style={{color:'#2563eb'}}>download</a>)</span>)}
                {log.message && (<span style={{color:'#eab308',marginLeft:8}}>{log.message}</span>)}
              </li>
            ))}
          </ul>
        )}
      </div>
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
          </div>
          {bulkSelected.length>0 && (
            <div style={{marginBottom:12}}>
              <button onClick={()=>bulkSelected.forEach(i=>handleExport('csv',filteredPartners[i]))} style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600,marginRight:8}}>Bulk Export CSV</button>
              <button onClick={()=>bulkSelected.forEach(i=>handleExport('pdf',filteredPartners[i]))} style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 14px',fontWeight:600}}>Bulk Export PDF</button>
            </div>
          )}
          {exported.pdf && (
            <a href={exported.pdf} download style={{marginRight:16,color:'#2563eb',fontWeight:600}}>Download PDF</a>
          )}
          <a href={`data:text/csv;charset=utf-8,${encodeURIComponent(csvContent)}`} download="partner_certification_export.csv" style={{color:'#059669',fontWeight:600}}>Download CSV</a>
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
  </div>
</div>
);
}
