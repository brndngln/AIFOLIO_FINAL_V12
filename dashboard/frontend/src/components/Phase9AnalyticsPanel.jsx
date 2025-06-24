import React, { useEffect, useState } from "react";

export default function Phase9AnalyticsPanel({ apiBase = "http://localhost:8090" }) {
  // --- Admin Session State ---
  const [sessionToken, setSessionToken] = useState(() => localStorage.getItem('phase9_session_token')||'');
  const [sessionExpires, setSessionExpires] = useState(0);
  const [showLogin, setShowLogin] = useState(!sessionToken);
  const [loginError, setLoginError] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginApiKey, setLoginApiKey] = useState("");
  const [loginMfa, setLoginMfa] = useState("");

  // --- Session Management ---
  useEffect(() => {
    if (!sessionToken) setShowLogin(true);
    else setShowLogin(false);
    if (sessionToken && sessionExpires > 0) {
      const timeout = setTimeout(() => {
        setSessionToken("");
        localStorage.removeItem('phase9_session_token');
        setShowLogin(true);
      }, sessionExpires * 1000);
      return () => clearTimeout(timeout);
    }
  }, [sessionToken, sessionExpires]);

  const handleLogin = async () => {
    setLoginLoading(true);
    setLoginError("");
    try {
      const res = await fetch(`${apiBase}/phase9/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: loginApiKey, mfa_code: loginMfa })
      });
      if (!res.ok) throw new Error('Login failed');
      const data = await res.json();
      setSessionToken(data.session_token);
      setSessionExpires(data.expires_in);
      localStorage.setItem('phase9_session_token', data.session_token);
      setShowLogin(false);
    } catch (e) {
      setLoginError("Invalid credentials or MFA");
    } finally {
      setLoginLoading(false);
    }
  };

  // --- Audit Log Widget State ---
  const [auditSearch, setAuditSearch] = useState("");
  const [auditFilterKey, setAuditFilterKey] = useState("");
  const [auditFilterAction, setAuditFilterAction] = useState("");
  const [auditFilterDate, setAuditFilterDate] = useState("");
  const [auditResults, setAuditResults] = useState([]);
  const [auditViolations, setAuditViolations] = useState([]);
  const [auditTotal, setAuditTotal] = useState(0);
  const [auditPage, setAuditPage] = useState(1);
  const [auditPageSize] = useState(50);
  const [auditLoading, setAuditLoading] = useState(false);
  const [showAuditStream, setShowAuditStream] = useState(false);

  // --- Key Management, Analytics, Compliance, etc. ---
  // Ensure all admin actions use session token in X-Session-Token header.

  // Add Key (admin, MFA, session)
  const handleAddKey = async (key, role, mfaCode) => {
    const res = await fetch(`${apiBase}/phase9/keys`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key, role, mfa_code: mfaCode })
    });
    if (!res.ok) throw new Error('Add key failed');
    return await res.json();
  };
  // Remove Key (admin, MFA, session)
  const handleRemoveKey = async (key, mfaCode) => {
    const res = await fetch(`${apiBase}/phase9/keys/${key}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mfa_code: mfaCode })
    });
    if (!res.ok) throw new Error('Remove key failed');
    return await res.json();
  };
  // Rotate Key (admin, MFA, session)
  const handleRotateKey = async (key, mfaCode) => {
    const res = await fetch(`${apiBase}/phase9/keys/rotate/${key}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mfa_code: mfaCode })
    });
    if (!res.ok) throw new Error('Rotate key failed');
    return await res.json();
  };
  // Bulk Import Keys (admin, MFA, session)
  const handleBulkImportKeys = async (keys, mfaCode) => {
    const res = await fetch(`${apiBase}/phase9/keys/bulk_import`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ keys, mfa_code: mfaCode })
    });
    if (!res.ok) throw new Error('Bulk import failed');
    return await res.json();
  };
  // Bulk Export Keys (admin, MFA, session)
  const handleBulkExportKeys = async (mfaCode) => {
    const res = await fetch(`${apiBase}/phase9/keys/bulk_export`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken,
        'mfa_code': mfaCode
      }
    });
    if (!res.ok) throw new Error('Bulk export failed');
    return await res.json();
  };

  // --- Audit Log Widget Handlers ---
  const handleAuditSearch = async () => {
    setAuditLoading(true);
    try {
      const filters = {};
      if (auditFilterKey) filters.key = auditFilterKey;
      if (auditFilterAction) filters.action = auditFilterAction;
      if (auditFilterDate) filters.date = auditFilterDate;
      const search = auditSearch ? { q: auditSearch } : undefined;
      const res = await fetch(`${apiBase}/phase9/audit_log/search`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
          'X-Session-Token': sessionToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filters, search, page: auditPage, page_size: auditPageSize })
      });
      if (!res.ok) throw new Error('Audit log search failed');
      const data = await res.json();
      setAuditResults(data.results||[]);
      setAuditViolations(data.violations||[]);
      setAuditTotal(data.total||0);
    } catch (e) {
      setAuditResults([]); setAuditViolations([]); setAuditTotal(0);
    } finally {
      setAuditLoading(false);
    }
  };
  useEffect(()=>{ handleAuditSearch(); /* auto-load on mount and page/filter change */ },[auditPage]);

  const handleAuditExport = async () => {
    const filters = {};
    if (auditFilterKey) filters.key = auditFilterKey;
    if (auditFilterAction) filters.action = auditFilterAction;
    if (auditFilterDate) filters.date = auditFilterDate;
    const params = new URLSearchParams();
    params.append('format','csv');
    // Optionally add filters/search as needed
    const url = `${apiBase}/phase9/audit_log/export?format=csv`;
    // Use fetch to include session token
    fetch(url, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key')||''}`,
        'X-Session-Token': sessionToken
      }
    }).then(async res => {
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = 'audit_log.csv';
      link.click();
    }).catch(()=>{});

  };

  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [endpointStats, setEndpointStats] = useState({});
  const [timeSeries, setTimeSeries] = useState({});
  const [perKeyStats, setPerKeyStats] = useState({});
  const [roleTimeSeries, setRoleTimeSeries] = useState({});
  const [perRoleStats, setPerRoleStats] = useState({});
  const [perStatusStats, setPerStatusStats] = useState({});
  const [latencyStats, setLatencyStats] = useState({});
  const [errorRate, setErrorRate] = useState({});
  const [complianceReport, setComplianceReport] = useState(null);
  const [csvUrl, setCsvUrl] = useState(null);
  const [jsonUrl, setJsonUrl] = useState(null);
  const [filter, setFilter] = useState({});
  const [search, setSearch] = useState({});
  const [timeRange, setTimeRange] = useState({start: '', end: ''});
  const [showExportModal, setShowExportModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [showComplianceModal, setShowComplianceModal] = useState(false);
  const [expandedKey, setExpandedKey] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [liveUpdate, setLiveUpdate] = useState(false);

  useEffect(() => {
    const fetchAll = () => {
      setLoading(true);
      fetch(`${apiBase}/phase9/analytics`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch analytics"))
        .then(setStats)
        .catch(e => setError(e.toString()))
        .finally(() => setLoading(false));
      fetch(`${apiBase}/phase9/analytics/endpoints`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch endpoint breakdown"))
        .then(setEndpointStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/timeseries`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch time series"))
        .then(setTimeSeries)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_key_breakdown`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-key breakdown"))
        .then(setPerKeyStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/role_time_series`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch role time series"))
        .then(setRoleTimeSeries)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_role`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-role breakdown"))
        .then(setPerRoleStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_status`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-status breakdown"))
        .then(setPerStatusStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/latency`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch latency stats"))
        .then(setLatencyStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/error_rate`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
          'X-Session-Token': sessionToken
        }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch error rate"))
        .then(setErrorRate)
        .catch(()=>{});
    };
    fetchAll();
    let interval = null;
    if (liveUpdate) interval = setInterval(fetchAll, 10000);
    return () => { if (interval) clearInterval(interval); };
  }, [apiBase, liveUpdate]);

  const handleFilter = async (f) => {
    setFilter(f);
    setLoading(true);
    setError(null);
    fetch(`${apiBase}/phase9/analytics/filter`, {
      method: "POST",
      headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(f)
    })
      .then(r => r.ok ? r.json() : Promise.reject("Failed to filter analytics"))
      .then(setStats)
      .catch(e => setError(e.toString()))
      .finally(() => setLoading(false));
  };

  const handleExport = async () => {
    const res = await fetch(`${apiBase}/phase9/analytics/export_csv`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` },
      method: 'GET',
    });
    if (!res.ok) return;
    const csv = await res.text();
    const blob = new Blob([csv], {type: 'text/csv'});
    setCsvUrl(URL.createObjectURL(blob));
  };
  const handleExportJSON = async () => {
    const res = await fetch(`${apiBase}/phase9/analytics/export_json`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` },
      method: 'GET',
    });
    if (!res.ok) return;
    const json = await res.text();
    const blob = new Blob([json], {type: 'application/json'});
    setJsonUrl(URL.createObjectURL(blob));
  };
  const handleComplianceReport = async () => {
    const res = await fetch(`${apiBase}/phase9/analytics/compliance_report`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`,
        'X-Session-Token': sessionToken,
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify({filters: filter, search, time_range: (timeRange.start && timeRange.end) ? [timeRange.start, timeRange.end] : undefined})
    });
    if (!res.ok) return;
    setComplianceReport(await res.json());
    setShowComplianceModal(true);
  };

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div style={{color:'red'}}>{error}</div>;

  return (
    <div style={{border:'1px solid #e7e', borderRadius:8, padding:16, marginBottom:24, background:darkMode?'#23202b':'#faf7ff', color:darkMode?'#fff':'#222'}} aria-label="Phase 9+ Analytics Panel">
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h3 tabIndex={0} aria-label="Phase 9+ Advanced Analytics">Phase 9+ Advanced Analytics</h3>
        <div>
          <button onClick={()=>setDarkMode(d=>!d)} aria-label="Toggle dark mode" style={{marginRight:8}}>{darkMode?'🌙':'☀️'}</button>
          <button onClick={()=>setLiveUpdate(l=>!l)} aria-label="Toggle live update" style={{marginRight:8}}>{liveUpdate?'⏸️':'▶️'}</button>
        </div>
      </div>
      <div style={{display:'flex',gap:18,alignItems:'flex-end',marginBottom:12,flexWrap:'wrap'}}>
        <label htmlFor="filter-key" style={{fontSize:13}}>Key: <input id="filter-key" aria-label="Filter by key" style={{width:90}} value={filter.key||''} onChange={e=>handleFilter({...filter,key:e.target.value||undefined})} /></label>
        <label htmlFor="filter-endpoint" style={{fontSize:13}}>Endpoint: <input id="filter-endpoint" aria-label="Filter by endpoint" style={{width:110}} value={filter.endpoint||''} onChange={e=>handleFilter({...filter,endpoint:e.target.value||undefined})} /></label>
        <label htmlFor="filter-role" style={{fontSize:13}}>Role: <input id="filter-role" aria-label="Filter by role" style={{width:80}} value={filter.role||''} onChange={e=>handleFilter({...filter,role:e.target.value||undefined})} /></label>
        <label htmlFor="filter-date" style={{fontSize:13}}>Date: <input id="filter-date" aria-label="Filter by date" type="date" style={{width:120}} value={filter.date||''} onChange={e=>handleFilter({...filter,date:e.target.value||undefined})} /></label>
        <label htmlFor="search-regex" style={{fontSize:13}}>Regex: <input id="search-regex" aria-label="Regex search" style={{width:100}} value={search.regex||''} onChange={e=>setSearch({...search,regex:e.target.value||undefined})} /></label>
        <label htmlFor="search-substring" style={{fontSize:13}}>Substring: <input id="search-substring" aria-label="Substring search" style={{width:100}} value={search.substring||''} onChange={e=>setSearch({...search,substring:e.target.value||undefined})} /></label>
        <label htmlFor="time-start" style={{fontSize:13}}>From: <input id="time-start" type="datetime-local" aria-label="Time range start" style={{width:170}} value={timeRange.start} onChange={e=>setTimeRange({...timeRange,start:e.target.value})} /></label>
        <label htmlFor="time-end" style={{fontSize:13}}>To: <input id="time-end" type="datetime-local" aria-label="Time range end" style={{width:170}} value={timeRange.end} onChange={e=>setTimeRange({...timeRange,end:e.target.value})} /></label>
        <button onClick={handleComplianceReport} aria-label="Generate compliance report" style={{marginLeft:8}}>Compliance Report</button>
        <button onClick={()=>setShowDetailsModal(true)} aria-label="Show advanced analytics details" style={{marginLeft:8}}>Details</button>
      </div>
      <ul style={{margin:0, paddingLeft:18, fontSize:14}}>
        <li tabIndex={0} aria-label="Total API Calls"><b title="Total API Calls">Total API Calls:</b> <span title="Total number of API calls">{stats.total_calls}</span></li>
        <li tabIndex={0} aria-label="Unique Keys Used"><b title="Unique Keys Used">Unique Keys Used:</b> <span title="Number of unique API keys">{stats.unique_keys}</span></li>
        <li tabIndex={0} aria-label="Most Active Key"><b title="Most Active Key">Most Active Key:</b> <span title="Key with most requests">{stats.most_active_key}</span></li>
        <li tabIndex={0} aria-label="Most Used Endpoint"><b title="Most Used Endpoint">Most Used Endpoint:</b> <span title="Most frequently called endpoint">{stats.most_used_endpoint}</span></li>
        <li tabIndex={0} aria-label="Calls by Role"><b title="Calls by Role">Calls by Role:</b> <span title="API calls grouped by role">{stats.calls_by_role && Object.entries(stats.calls_by_role).map(([role, n]) => `${role}: ${n}`).join(", ")}</span></li>
        <li tabIndex={0} aria-label="Last 24h Calls"><b title="Last 24h Calls">Last 24h Calls:</b> <span title="API calls in the last 24 hours">{stats.last_24h_calls}</span></li>
      </ul>
      <div style={{marginTop:18, marginBottom:8}}>
        <b>Endpoint Breakdown</b>
        <table style={{fontSize:13, marginTop:4, background:'#fff', border:'1px solid #eee', borderRadius:4}} aria-label="Endpoint Breakdown">
          <thead><tr><th style={{textAlign:'left',padding:'2px 8px'}}>Endpoint</th><th style={{textAlign:'right',padding:'2px 8px'}}>Calls</th></tr></thead>
          <tbody>
            {Object.entries(endpointStats).map(([ep, n]) => (
              <tr key={ep}><td style={{padding:'2px 8px'}}>{ep}</td><td style={{padding:'2px 8px',textAlign:'right'}}>{n}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{margin:'16px 0'}}>
        <b>API Calls Over Time</b>
        <div style={{display:'flex',alignItems:'flex-end',height:60,gap:2,background:'#f5f4fa',borderRadius:4,padding:'8px 6px'}} aria-label="API Calls Over Time">
          {Object.entries(timeSeries).map(([day, n]) => (
            <div key={day} title={day+': '+n} style={{height:Math.max(4,Math.min(48,n)),width:10,background:'#a7c',borderRadius:2,display:'inline-block',marginRight:2}} aria-label={`Date ${day}, ${n} calls`}></div>
          ))}
        </div>
        <div style={{fontSize:11, color:'#888', marginTop:2}}>
          {Object.keys(timeSeries).map(day => <span key={day} style={{marginRight:8}}>{day}</span>)}
        </div>
      </div>
      <div style={{margin:'20px 0'}}>
        <b>Per-Key Endpoint Breakdown</b>
        <table style={{fontSize:12, background:'#fff', border:'1px solid #eee', borderRadius:4, width:'100%'}} aria-label="Per-Key Endpoint Breakdown">
          <thead><tr><th>Key</th><th>Role</th><th>Endpoints</th></tr></thead>
          <tbody>
            {Object.entries(perKeyStats).map(([key, eps]) => (
              <tr key={key}>
                <td style={{fontFamily:'monospace'}}>{key}</td>
                <td>{/* Role lookup not shown here for brevity */}</td>
                <td>
                  <button aria-label={`Expand endpoints for ${key}`} onClick={()=>setExpandedKey(expandedKey===key?null:key)}>{expandedKey===key?'Hide':'Show'}</button>
                  {expandedKey===key && (
                    <ul style={{margin:0,paddingLeft:12}}>
                      {Object.entries(eps).map(([ep, n]) => <li key={ep}><span style={{fontFamily:'monospace'}}>{ep}</span>: {n}</li>)}
                    </ul>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={{margin:'20px 0'}}>
        <b>Role-based API Calls Over Time</b>
        <div style={{display:'flex',alignItems:'flex-end',height:60,gap:2,background:'#f5f4fa',borderRadius:4,padding:'8px 6px'}} aria-label="Role-based API Calls Over Time">
          {Object.entries(roleTimeSeries).map(([day, roleCounts]) => (
            <div key={day} style={{display:'flex',flexDirection:'column',width:16}} title={day}>
              {Object.entries(roleCounts).map(([role, n]) => (
                <div key={role} style={{height:Math.max(2,Math.min(48,n)),background:role==="admin"?"#27b36a":role==="viewer"?"#2a7fd3":role==="auditor"?"#b77fd3":role==="maintainer"?"#e6b800":"#bbb",width:'100%',marginBottom:1}} title={role+': '+n} aria-label={`Role ${role}, ${n} calls`}></div>
              ))}
            </div>
          ))}
        </div>
        <div style={{fontSize:11, color:'#888', marginTop:2}}>
          {Object.keys(roleTimeSeries).map(day => <span key={day} style={{marginRight:8}}>{day}</span>)}
        </div>
      </div>
      <div style={{display:'flex',gap:8,marginTop:10,marginBottom:4}}>
        <button onClick={()=>setShowExportModal(true)} aria-label="Export CSV">Export CSV</button>
        <button onClick={handleExportJSON} aria-label="Export JSON">Export JSON</button>
        <button onClick={handleComplianceReport} aria-label="Show compliance report">Compliance Report</button>
      </div>
      {csvUrl && <a href={csvUrl} download="phase9_audit_log.csv" style={{marginLeft:8}}>Download CSV</a>}
      {jsonUrl && <a href={jsonUrl} download="phase9_audit_log.json" style={{marginLeft:8}}>Download JSON</a>}
      {/* Latency stats visualization */}
      <div style={{margin:'20px 0'}}>
        <b>Latency Stats <span title="API response time per endpoint (ms)">🛈</span></b>
        <table style={{fontSize:12, background:darkMode?'#222':'#fff', color:darkMode?'#fff':'#222', border:'1px solid #eee', borderRadius:4, width:'100%'}} aria-label="Latency Stats">
          <thead><tr><th>Endpoint</th><th>Min</th><th>Avg</th><th>Median</th><th>Max</th><th>P95</th></tr></thead>
          <tbody>
            {Object.entries(latencyStats).map(([ep, stats]) => (
              <tr key={ep}>
                <td style={{fontFamily:'monospace'}}>{ep}</td>
                <td>{stats.min}</td>
                <td>{stats.avg && stats.avg.toFixed ? stats.avg.toFixed(1) : stats.avg}</td>
                <td>{stats.median}</td>
                <td>{stats.max}</td>
                <td>{stats.p95 && stats.p95.toFixed ? stats.p95.toFixed(1) : stats.p95}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Error rate visualization */}
      <div style={{margin:'20px 0'}}>
        <b>Error Rate <span title="Proportion of 4xx/5xx responses">🛈</span></b>
        <div style={{fontSize:13}}>
          {errorRate && typeof errorRate.error_rate === 'number' && (
            <span>{errorRate.error_count} errors ({(errorRate.error_rate*100).toFixed(2)}%)</span>
          )}
        </div>
      </div>
      {/* Per-role endpoint breakdown */}
      <div style={{margin:'20px 0'}}>
        <b>Per-Role Endpoint Breakdown <span title="API usage by role and endpoint">🛈</span></b>
        <table style={{fontSize:12, background:darkMode?'#222':'#fff', color:darkMode?'#fff':'#222', border:'1px solid #eee', borderRadius:4, width:'100%'}} aria-label="Per-Role Endpoint Breakdown">
          <thead><tr><th>Role</th><th>Endpoint</th><th>Calls</th></tr></thead>
          <tbody>
            {Object.entries(perRoleStats).flatMap(([role, eps]) => (
              Object.entries(eps).map(([ep, n]) => (
                <tr key={role+ep}><td>{role}</td><td>{ep}</td><td>{n}</td></tr>
              ))
            ))}
          </tbody>
        </table>
      </div>
      {/* Per-status endpoint breakdown */}
      <div style={{margin:'20px 0'}}>
        <b>Per-Status Endpoint Breakdown <span title="API usage by status and endpoint">🛈</span></b>
        <table style={{fontSize:12, background:darkMode?'#222':'#fff', color:darkMode?'#fff':'#222', border:'1px solid #eee', borderRadius:4, width:'100%'}} aria-label="Per-Status Endpoint Breakdown">
          <thead><tr><th>Status</th><th>Endpoint</th><th>Calls</th></tr></thead>
          <tbody>
            {Object.entries(perStatusStats).flatMap(([status, eps]) => (
              Object.entries(eps).map(([ep, n]) => (
                <tr key={status+ep}><td>{status}</td><td>{ep}</td><td>{n}</td></tr>
              ))
            ))}
          </tbody>
        </table>
      </div>
      {/* Compliance report modal */}
      {showComplianceModal && complianceReport && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:10000}}>
          <div style={{background:'#fff',padding:24,borderRadius:8,minWidth:320,maxWidth:600,color:'#222'}}>
            <h4>Compliance Report</h4>
            <pre style={{fontSize:13,whiteSpace:'pre-wrap',wordBreak:'break-all',background:'#f7f7f7',padding:12,borderRadius:4}}>{JSON.stringify(complianceReport,null,2)}</pre>
            <button onClick={()=>setShowComplianceModal(false)}>Close</button>
          </div>
        </div>
      )}
      {showExportModal && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:10000}}>
          <div style={{background:'#fff',padding:24,borderRadius:8,minWidth:320}}>
            <h4>Export Audit Log CSV</h4>
            <p>Download the full audit log as a CSV file for compliance or external analysis.</p>
            <button onClick={handleExport} style={{marginRight:12}}>Generate CSV</button>
            <button onClick={handleExportJSON} style={{marginRight:12}}>Generate JSON</button>
            <button onClick={()=>setShowExportModal(false)}>Close</button>
            {csvUrl && <div style={{marginTop:10}}><a href={csvUrl} download="phase9_audit_log.csv">Download CSV</a></div>}
            {jsonUrl && <div style={{marginTop:10}}><a href={jsonUrl} download="phase9_audit_log.json">Download JSON</a></div>}
          </div>
        </div>
      )}
      {showDetailsModal && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:10000}}>
          <div style={{background:'#fff',padding:24,borderRadius:8,minWidth:320,maxWidth:600}}>
            <h4>Advanced Analytics Details</h4>
            <ul>
              <li>Per-key endpoint breakdown: See which endpoints are most used by each API key.</li>
              <li>Role-based time series: Track API usage by role over time.</li>
              <li>Latency stats: See API response times per endpoint.</li>
              <li>Error rate: Track error frequency and compliance risk.</li>
              <li>Per-role and per-status breakdowns: Deep compliance and usage analysis.</li>
              <li>Filter, search, and export any view.</li>
              <li>All metrics are accessible and keyboard-navigable.</li>
              <li>Dark mode, live updating, and onboarding tooltips included.</li>
            </ul>
            <button onClick={()=>setShowDetailsModal(false)}>Close</button>
          </div>
        </div>
      )}
      {/* --- Admin Help & Onboarding --- */}
      <div style={{margin:'16px 0',padding:'10px',border:'1px solid #b3d4fc',borderRadius:6,background:'#eaf4ff',color:'#195080',fontSize:14}}>
        <b>Admin Onboarding:</b> All actions require valid API key, MFA, and session. Sessions expire after 15 minutes. <span title="Learn more about SAFE AI compliance" style={{textDecoration:'underline',cursor:'pointer'}} onClick={()=>setShowHelp(true)}>Help</span>
      </div>
      {showHelp && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.6)',zIndex:10001,display:'flex',alignItems:'center',justifyContent:'center'}}>
          <div style={{background:'#fff',color:'#222',padding:24,borderRadius:10,maxWidth:480,boxShadow:'0 2px 12px #0003'}}>
            <h3>SAFE AI Admin Compliance Help</h3>
            <ul style={{fontSize:15,lineHeight:1.7}}>
              <li>All admin actions are statically logged for audit and compliance.</li>
              <li>Session tokens are required for every sensitive operation.</li>
              <li>MFA (TOTP) is enforced for all key management and export actions.</li>
              <li>Compliance violations are highlighted in audit logs and analytics.</li>
              <li>Charts and tables can be exported for compliance documentation.</li>
              <li>All UI is accessible, responsive, and SAFE AI Charter compliant.</li>
            </ul>
            <button onClick={()=>setShowHelp(false)} style={{marginTop:8}}>Close</button>
          </div>
        </div>
      )}

      {/* --- PHASE 10+ TENANT/WHITE-LABEL CONTROLS --- */}
      <div style={{margin:'20px 0',padding:'10px',border:'1px solid #d4eaff',borderRadius:7,background:'#fafdff',color:'#195080'}}>
        <b>Tenant/Brand Switcher:</b> <span style={{fontSize:12}}>(Multi-tenant, white-label, static)</span>
        <div style={{margin:'8px 0'}}>
          <select value={tenantId} onChange={e=>setTenantId(e.target.value)} aria-label="Select Tenant">
            {tenantList.map(t=>(<option value={t.id} key={t.id}>{t.name}</option>))}
          </select>
          <span style={{marginLeft:10}}>
            {tenantConfig.logo && <img src={tenantConfig.logo} alt="Logo" style={{height:24,verticalAlign:'middle',marginRight:8}}/>}
            <b style={{color:tenantConfig.color}}>{tenantConfig.name}</b>
          </span>
        </div>
        <div style={{fontSize:13,margin:'6px 0'}}>
          <span title="SAFE AI Compliance Statement">🛡️</span> {tenantConfig.compliance_statement}
        </div>
        <div style={{fontSize:12,margin:'4px 0'}}>
          {tenantConfig.legal_docs && tenantConfig.legal_docs.map((l,i)=>(<a key={i} href={l} target="_blank" rel="noopener noreferrer" style={{marginRight:8}}>{l.replace('/legal/','').replace('.md','').replace('_',' ').toUpperCase()}</a>))}
        </div>
        <div style={{marginTop:8}}>
          <b>Enabled Modules:</b> {enabledModules.join(', ')}
        </div>
        <div style={{marginTop:8}}>
          {/* Admin-only: Module toggles */}
          {isAdmin && Object.keys(allModules).map(m=>(
            <label key={m} style={{marginRight:10}}>
              <input type="checkbox" checked={enabledModules.includes(m)} onChange={e=>toggleModule(m,e.target.checked)} aria-label={`Toggle module ${m}`}/>
              {allModules[m]}
            </label>
          ))}
        </div>
      </div>
      {/* --- PHASE 10+ WEBHOOKS, REPORTING, ADVANCED INTEGRATIONS --- */}
      <div style={{margin:'22px 0',padding:'13px',border:'1px solid #e5e5e5',borderRadius:7,background:'#f8fafd',color:'#1a3c60'}}>
        <b>Custom Hooks & Advanced Reporting</b> <span style={{fontSize:12}}>(SAFE AI, static, white-label, future-proof)</span>
        <div style={{margin:'10px 0',padding:'8px',background:'#eef7fa',borderRadius:6}}>
          <b>Webhook Management</b> <span title="Configure outbound webhooks for compliance, vault, onboarding, admin events">🪝</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const res = await fetch(`${apiBase}/phase10/webhook/get?tenant_id=${tenantId}`);
              alert('Webhooks: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="View Webhook Config">View Config</button>
            {['compliance','vault_export','onboarding','admin_action'].map(ev=>(
              <button key={ev} onClick={async()=>{
                const url = prompt(`Set webhook URL for event '${ev}'`);
                if (!url) return;
                await fetch(`${apiBase}/phase10/webhook/set`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,event:ev,url})});
                alert('Webhook set.');
              }} aria-label={`Set webhook for ${ev}`}>Set {ev}</button>
            ))}
            {['compliance','vault_export','onboarding','admin_action'].map(ev=>(
              <button key={ev+"trigger"} onClick={async()=>{
                const payload = {timestamp:Date.now(),event:ev,tenant:tenantId};
                const res = await fetch(`${apiBase}/phase10/webhook/trigger`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,event:ev,payload})});
                alert('Webhook Triggered: '+JSON.stringify(await res.json(),null,2));
              }} aria-label={`Trigger webhook for ${ev}`}>Trigger {ev}</button>
            ))}
          </div>
        </div>
        <div style={{margin:'10px 0',padding:'8px',background:'#f3f7f0',borderRadius:6}}>
          <b>Custom Report Builder</b> <span title="Build custom analytics/compliance/finance reports per tenant">📄</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const mods = prompt('Enter modules (comma separated, e.g. vault,analytics,compliance)');
              const fields = prompt('Enter fields (comma separated, e.g. balance,compliance_status,forecast)');
              if (!mods || !fields) return;
              const modules = mods.split(',').map(x=>x.trim());
              const flds = fields.split(',').map(x=>x.trim());
              const res = await fetch(`${apiBase}/phase10/report/custom`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,modules,flds})});
              const data = await res.json();
              alert('Custom Report: '+JSON.stringify(data,null,2));
            }} aria-label="Build Custom Report">Build Report</button>
            <button onClick={async()=>{
              const mods = prompt('Export modules (comma separated)');
              const fields = prompt('Export fields (comma separated)');
              const format = prompt('Export format (pdf, csv, json)');
              if (!mods || !fields || !format) return;
              // Simulate export (static)
              alert(`Exported report for modules: ${mods}, fields: ${fields}, format: ${format}`);
            }} aria-label="Export Custom Report">Export Report</button>
          </div>
        </div>
        <div style={{margin:'10px 0',padding:'8px',background:'#f9f7f0',borderRadius:6}}>
          <b>Scheduled Reporting</b> <span title="Configure static scheduled reports per tenant">⏰</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const schedule = prompt('Enter schedule (e.g. daily, weekly, cron)');
              if (!schedule) return;
              await fetch(`${apiBase}/phase10/report/schedule`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,schedule:{type:schedule}})});
              alert('Schedule set.');
            }} aria-label="Set Report Schedule">Set Schedule</button>
            <button onClick={async()=>{
              alert('Static: Schedule is set per admin input, not persisted.');
            }} aria-label="View Report Schedule">View Schedule</button>
          </div>
        </div>
        <div style={{margin:'10px 0',padding:'8px',background:'#f7f3fa',borderRadius:6}}>
          <b>SaaS Integrations</b> <span title="Export or notify via Stripe, Notion, Slack, XBRL">🔌</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const res = await fetch(`${apiBase}/phase10/integrations/stripe?tenant_id=${tenantId}`);
              alert('Stripe Transactions: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="Export Stripe Transactions" title="Export static Stripe transactions for tenant">Stripe Export</button>
            <button onClick={async()=>{
              const res = await fetch(`${apiBase}/phase10/integrations/notion?tenant_id=${tenantId}`);
              alert('Notion Data: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="Export Notion Data" title="Export static Notion data for tenant">Notion Export</button>
            <button onClick={async()=>{
              const msg = prompt('Enter Slack message to send');
              if (!msg) return;
              const res = await fetch(`${apiBase}/phase10/integrations/slack`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,message:msg})});
              alert('Slack Notification: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="Send Slack Notification" title="Send static Slack notification for tenant">Slack Notify</button>
            <button onClick={async()=>{
              const res = await fetch(`${apiBase}/phase10/integrations/xbrl?tenant_id=${tenantId}`);
              alert('XBRL Report: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="Export XBRL Report" title="Export static XBRL report for tenant">XBRL Export</button>
          </div>
        </div>
      </div>
      {/* --- PHASE 10+ NEURO CORE & EMPIRE COMMAND --- */}
      <div style={{margin:'22px 0',padding:'13px',border:'1px solid #e5e5e5',borderRadius:7,background:'#f8fafd',color:'#1a3c60'}}>
        <b>Custom Hooks & Advanced Reporting</b> <span style={{fontSize:12}}>(SAFE AI, static, white-label, future-proof)</span>
        <div style={{margin:'10px 0',padding:'8px',background:'#eef7fa',borderRadius:6}}>
          <b>Webhook Management</b> <span title="Configure outbound webhooks for compliance, vault, onboarding, admin events">🪝</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const res = await fetch(`${apiBase}/phase10/webhook/get?tenant_id=${tenantId}`);
              alert('Webhooks: '+JSON.stringify(await res.json(),null,2));
            }} aria-label="View Webhook Config">View Config</button>
            {['compliance','vault_export','onboarding','admin_action'].map(ev=>(
              <button key={ev} onClick={async()=>{
                const url = prompt(`Set webhook URL for event '${ev}'`);
                if (!url) return;
                await fetch(`${apiBase}/phase10/webhook/set`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,event:ev,url})});
                alert('Webhook set.');
              }} aria-label={`Set webhook for ${ev}`}>Set {ev}</button>
            ))}
            {['compliance','vault_export','onboarding','admin_action'].map(ev=>(
              <button key={ev+"trigger"} onClick={async()=>{
                const payload = {timestamp:Date.now(),event:ev,tenant:tenantId};
                const res = await fetch(`${apiBase}/phase10/webhook/trigger`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,event:ev,payload})});
                alert('Webhook Triggered: '+JSON.stringify(await res.json(),null,2));
              }} aria-label={`Trigger webhook for ${ev}`}>Trigger {ev}</button>
            ))}
          </div>
        </div>
        <div style={{margin:'10px 0',padding:'8px',background:'#f3f7f0',borderRadius:6}}>
          <b>Custom Report Builder</b> <span title="Build custom analytics/compliance/finance reports per tenant">📄</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const mods = prompt('Enter modules (comma separated, e.g. vault,analytics,compliance)');
              const fields = prompt('Enter fields (comma separated, e.g. balance,compliance_status,forecast)');
              if (!mods || !fields) return;
              const modules = mods.split(',').map(x=>x.trim());
              const flds = fields.split(',').map(x=>x.trim());
              const res = await fetch(`${apiBase}/phase10/report/custom`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,modules,flds})});
              const data = await res.json();
              alert('Custom Report: '+JSON.stringify(data,null,2));
            }} aria-label="Build Custom Report">Build Report</button>
            <button onClick={async()=>{
              const mods = prompt('Export modules (comma separated)');
              const fields = prompt('Export fields (comma separated)');
              const format = prompt('Export format (pdf, csv, json)');
              if (!mods || !fields || !format) return;
              // Simulate export (static)
              alert(`Exported report for modules: ${mods}, fields: ${fields}, format: ${format}`);
            }} aria-label="Export Custom Report">Export Report</button>
          </div>
        </div>
        <div style={{margin:'10px 0',padding:'8px',background:'#f9f7f0',borderRadius:6}}>
          <b>Scheduled Reporting</b> <span title="Configure static scheduled reports per tenant">⏰</span>
          <div style={{display:'flex',gap:8,flexWrap:'wrap',alignItems:'center',margin:'6px 0'}}>
            <button onClick={async()=>{
              const schedule = prompt('Enter schedule (e.g. daily, weekly, cron)');
              if (!schedule) return;
              await fetch(`${apiBase}/phase10/report/schedule`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:tenantId,schedule:{type:schedule}})});
              alert('Schedule set.');
            }} aria-label="Set Report Schedule">Set Schedule</button>
            <button onClick={async()=>{
              alert('Static: Schedule is set per admin input, not persisted.');
            }} aria-label="View Report Schedule">View Schedule</button>
          </div>
        </div>
      </div>
      {/* --- PHASE 10+ NEURO CORE & EMPIRE COMMAND --- */}
      <div style={{margin:'24px 0',padding:'14px',border:'1px solid #b3d4fc',borderRadius:7,background:'#f5faff',color:'#195080'}}>
        <b>PHASE 10+ EMPIRE COMMANDS:</b> <span style={{fontSize:12}}>(SAFE AI, static, read-only, future-proof)</span>
        <div style={{display:'flex',flexWrap:'wrap',gap:8,marginTop:8}}>
          <button onClick={async()=>{
            const res = await fetch(`${apiBase}/phase10/neuro_core/export_analytics`); alert(JSON.stringify(await res.json(),null,2));
          }} aria-label="Export Analytics to NEURO CORE" title="Export static analytics and forecasts to NEURO CORE">Export Analytics</button>
          <button onClick={async()=>{
            const res = await fetch(`${apiBase}/phase10/neuro_core/export_memory_grid`); alert(JSON.stringify(await res.json(),null,2));
          }} aria-label="Export Memory Grid" title="Export static memory grid to NEURO CORE">Export Memory Grid</button>
          <button onClick={async()=>{
            const res = await fetch(`${apiBase}/phase10/neuro_core/revenue_health_feed`); alert(JSON.stringify(await res.json(),null,2));
          }} aria-label="Export Revenue/Health Feed" title="Export cross-brand revenue and health feed">Export Revenue/Health</button>
          <button onClick={async()=>{
            const token = prompt('Enter NEURO CORE Admin Token:');
            if (!token) return;
            const res = await fetch(`${apiBase}/phase10/neuro_core/validate_admin_token`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token})});
            alert('Token valid: '+((await res.json()).valid));
          }} aria-label="Validate NEURO CORE Admin Token" title="Validate NEURO CORE admin token (static, SAFE AI Charter enforced)">Validate Admin Token</button>
        </div>
        <div style={{marginTop:12,fontSize:13}}>
          <span title="SAFE AI Empire Financials">💰</span> <b>Vault/Finance:</b>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/global_vault`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="View Global Vault">Global Vault</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/total_vault`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="View Total Vault">Total Vault</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/forecast`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="View Financial Forecast">Forecast</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/risk_firewall`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Check Risk Firewall">Risk Firewall</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/optimizer`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Run Capital Optimizer">Optimizer</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/finance/reinvestment_plan`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Get Reinvestment Plan">Reinvestment</button>
        </div>
        <div style={{marginTop:12,fontSize:13}}>
          <span title="SAFE AI Strategic Meta-Command">🧠</span> <b>Meta-Command:</b>
          <button onClick={async()=>{const markets={AIFOLIO:100,QuantumTraderAI:120};const res=await fetch(`${apiBase}/phase10/meta/arbitrage_scan`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({markets})});alert(JSON.stringify(await res.json(),null,2));}} aria-label="Scan Arbitrage">Arbitrage</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/meta/vault_rotation`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Suggest Vault Rotation">Vault Rotation</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/meta/reserve_rebalancer`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Rebalance Reserves">Reserve Rebalancer</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/meta/liquidity_funnel`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Liquidity Funnel">Liquidity Funnel</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/meta/synthetic_capital_grid`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Synthetic Capital Grid">Synthetic Capital Grid</button>
        </div>
        <div style={{marginTop:12,fontSize:13}}>
          <span title="SAFE AI Legal & Governance">⚖️</span> <b>Legal/Governance:</b>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/legal/policy_mesh`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="View Policy Mesh">Policy Mesh</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/legal/jurisdiction_matrix`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="View Jurisdiction Matrix">Jurisdiction Matrix</button>
          <button onClick={async()=>{const revenue={US:100000,EU:90000};const res=await fetch(`${apiBase}/phase10/legal/tax_harmonization`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({revenue})});alert(JSON.stringify(await res.json(),null,2));}} aria-label="Harmonize Taxes">Tax Harmonization</button>
          <button onClick={async()=>{const events={AIFOLIO:'regulatory',QuantumTraderAI:'ok'};const res=await fetch(`${apiBase}/phase10/legal/legal_pressure_monitor`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({events})});alert(JSON.stringify(await res.json(),null,2));}} aria-label="Detect Legal Pressure">Legal Pressure</button>
          <button onClick={async()=>{const events={AIFOLIO:'expiry',QuantumTraderAI:'ok'};const res=await fetch(`${apiBase}/phase10/legal/legal_horizon_monitor`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({events})});alert(JSON.stringify(await res.json(),null,2));}} aria-label="Monitor Legal Horizon">Legal Horizon</button>
        </div>
        <div style={{marginTop:12,fontSize:13}}>
          <span title="SAFE AI Charter Enforcement">🛡️</span> <b>Charter/Lockout:</b>
          <button onClick={async()=>{try{await fetch(`${apiBase}/phase10/charter/enforce`);}catch(e){alert('Charter enforcement is permanent. No bypass allowed.');}}} aria-label="Enforce Charter">Enforce Charter</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/charter/lockout_test`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Run Lockout Test">Lockout Test</button>
          <button onClick={async()=>{const res=await fetch(`${apiBase}/phase10/charter/verification_log`);alert(JSON.stringify(await res.json(),null,2));}} aria-label="Generate Verification Log">Verification Log</button>
        </div>
      </div>
      {/* --- Chart/Image Download Option --- */}
      <div style={{marginBottom:16,display:'flex',justifyContent:'flex-end'}}>
        <button onClick={()=>{
          const chart = document.querySelector('.main-analytics-chart');
          if (!chart) return;
          import('html-to-image').then(htmlToImage => {
            htmlToImage.toPng(chart).then(dataUrl => {
              const link = document.createElement('a');
              link.download = 'analytics_chart.png';
              link.href = dataUrl;
              link.click();
            });
          });
        }} aria-label="Download analytics chart as image">Download Chart</button>
      </div>
      {/* --- Audit Log Widget --- */}
      <div style={{margin:'30px 0',padding:'16px',border:'1px solid #ddd',borderRadius:8,background:darkMode?'#181a1b':'#fdfdff'}}>
        <h4 style={{marginBottom:8}}>Audit Log Search & Export <span title="Advanced filtering, compliance highlighting, export, and live stream">🛈</span></h4>
        <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:8}}>
          <input value={auditSearch} onChange={e=>setAuditSearch(e.target.value)} placeholder="Search (substring/regex)" style={{width:180}} aria-label="Audit log search" />
          <input value={auditFilterKey} onChange={e=>setAuditFilterKey(e.target.value)} placeholder="Key filter" style={{width:120}} aria-label="Key filter" />
          <input value={auditFilterAction} onChange={e=>setAuditFilterAction(e.target.value)} placeholder="Action filter" style={{width:120}} aria-label="Action filter" />
          <input type="date" value={auditFilterDate} onChange={e=>setAuditFilterDate(e.target.value)} aria-label="Date filter" />
          <button onClick={handleAuditSearch} aria-label="Search audit log">Search</button>
          <button onClick={handleAuditExport} aria-label="Export filtered audit log">Export</button>
          <button onClick={()=>setShowAuditStream(s=>!s)} aria-label="Toggle live audit log stream">{showAuditStream?'Stop Live':'Live Stream'}</button>
        </div>
        {auditLoading && <div>Loading...</div>}
        <div style={{maxHeight:200,overflow:'auto',background:darkMode?'#222':'#fff',border:'1px solid #eee',borderRadius:5}} aria-label="Audit log results">
          {auditResults.length===0 && !auditLoading && <div style={{padding:8,color:'#aaa'}}>No results.</div>}
          <ul style={{margin:0,padding:8}}>
            {auditResults.map((entry,i)=>(
              <li key={i} style={{fontFamily:'monospace',fontSize:12,background:entry.match(/violation|noncompliance|SAFE AI Charter/i)?'#ffeaea':'',color:entry.match(/violation|noncompliance|SAFE AI Charter/i)?'#b30000':darkMode?'#fff':'#222',padding:'2px 0'}}>{entry}
                {entry.match(/SAFE AI Charter/i) && <span title="Charter violation" style={{marginLeft:6,color:'#b30000',fontWeight:600}} aria-label="Charter violation">⚠️</span>}
              </li>
            ))}
          </ul>
        </div>
        <div style={{marginTop:8,display:'flex',gap:8,alignItems:'center'}}>
          <span>Page {auditPage} / {Math.ceil(auditTotal/auditPageSize)||1}</span>
          <button onClick={()=>setAuditPage(p=>Math.max(1,p-1))} disabled={auditPage===1}>Prev</button>
          <button onClick={()=>setAuditPage(p=>p+1)} disabled={auditPage*auditPageSize>=auditTotal}>Next</button>
          <span style={{marginLeft:12}}>Violations: {auditViolations.length}</span>
        </div>
        {showAuditStream && (
          <div style={{marginTop:10}}>
            <iframe title="Live Audit Log" src="/phase9/audit_log/stream" style={{width:'100%',height:100,border:'1px solid #ccc',background:'#000',color:'#fff'}}></iframe>
          </div>
        )}
      </div>
    </div>
  );
}
