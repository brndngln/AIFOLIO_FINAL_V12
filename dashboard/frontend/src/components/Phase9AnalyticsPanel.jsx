import React, { useEffect, useState } from "react";

export default function Phase9AnalyticsPanel({ apiBase = "http://localhost:8090" }) {
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [endpointStats, setEndpointStats] = useState({});
  const [timeSeries, setTimeSeries] = useState({});
  const [csvUrl, setCsvUrl] = useState(null);

  useEffect(() => {
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
  }, [apiBase]);

  const handleExport = async () => {
    const res = await fetch(`${apiBase}/phase9/analytics/export_csv`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
    });
    if (!res.ok) return;
    const csv = await res.text();
    const blob = new Blob([csv], {type: 'text/csv'});
    setCsvUrl(URL.createObjectURL(blob));
  };

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div style={{color:'red'}}>{error}</div>;

  return (
    <div style={{border:'1px solid #e7e', borderRadius:8, padding:16, marginBottom:24, background:'#faf7ff'}}>
      <h3>Phase 9+ Advanced Analytics</h3>
      <ul style={{margin:0, paddingLeft:18, fontSize:14}}>
        <li><b>Total API Calls:</b> {stats.total_calls}</li>
        <li><b>Unique Keys Used:</b> {stats.unique_keys}</li>
        <li><b>Most Active Key:</b> {stats.most_active_key}</li>
        <li><b>Most Used Endpoint:</b> {stats.most_used_endpoint}</li>
        <li><b>Calls by Role:</b> {stats.calls_by_role && Object.entries(stats.calls_by_role).map(([role, n]) => `${role}: ${n}`).join(", ")}</li>
        <li><b>Last 24h Calls:</b> {stats.last_24h_calls}</li>
      </ul>
      <div style={{marginTop:18, marginBottom:8}}>
        <b>Endpoint Breakdown</b>
        <table style={{fontSize:13, marginTop:4, background:'#fff', border:'1px solid #eee', borderRadius:4}}>
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
        <div style={{display:'flex',alignItems:'flex-end',height:60,gap:2,background:'#f5f4fa',borderRadius:4,padding:'8px 6px'}}>
          {Object.entries(timeSeries).map(([day, n]) => (
            <div key={day} title={day+': '+n} style={{height:Math.max(4,Math.min(48,n)),width:10,background:'#a7c',borderRadius:2,display:'inline-block',marginRight:2}}></div>
          ))}
        </div>
        <div style={{fontSize:11, color:'#888', marginTop:2}}>
          {Object.keys(timeSeries).map(day => <span key={day} style={{marginRight:8}}>{day}</span>)}
        </div>
      </div>
      <button onClick={handleExport} style={{marginTop:10,marginBottom:4}}>Export CSV</button>
      {csvUrl && <a href={csvUrl} download="phase9_audit_log.csv" style={{marginLeft:8}}>Download</a>}
    </div>
  );
}
