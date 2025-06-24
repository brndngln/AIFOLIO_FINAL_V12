import React, { useEffect, useState } from "react";

export default function Phase9AnalyticsPanel({ apiBase = "http://localhost:8090" }) {
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
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch analytics"))
        .then(setStats)
        .catch(e => setError(e.toString()))
        .finally(() => setLoading(false));
      fetch(`${apiBase}/phase9/analytics/endpoints`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch endpoint breakdown"))
        .then(setEndpointStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/timeseries`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch time series"))
        .then(setTimeSeries)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_key_breakdown`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-key breakdown"))
        .then(setPerKeyStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/role_time_series`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch role time series"))
        .then(setRoleTimeSeries)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_role`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-role breakdown"))
        .then(setPerRoleStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/per_status`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch per-status breakdown"))
        .then(setPerStatusStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/latency`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      })
        .then(r => r.ok ? r.json() : Promise.reject("Failed to fetch latency stats"))
        .then(setLatencyStats)
        .catch(()=>{});
      fetch(`${apiBase}/phase9/analytics/error_rate`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
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
      headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`, 'Content-Type': 'application/json' },
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
    </div>
  );
}
