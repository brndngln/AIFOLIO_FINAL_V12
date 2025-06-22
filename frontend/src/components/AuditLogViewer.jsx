import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AuditLogViewer({ token }) {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios.get("/admin/audit-log", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => setLogs(res.data))
      .catch(() => setLogs([]))
      .finally(() => setLoading(false));
  }, [token]);

  const [userFilter, setUserFilter] = useState("");

  const filteredLogs = userFilter
    ? logs.filter(entry => entry.user && entry.user.includes(userFilter))
    : logs;

  return (
    <div className="audit-log-viewer" aria-label="SAFE AI Audit Log" tabIndex={0} style={{background:'#f8fafc',padding:20,borderRadius:8}}>
      <h3 style={{color:'#0f172a'}}>SAFE AI Audit Log</h3>
      <label htmlFor="user-filter" style={{fontWeight:600}}>Filter by user:</label>
      <input
        id="user-filter"
        aria-label="Filter by user"
        value={userFilter}
        onChange={e => setUserFilter(e.target.value)}
        style={{marginLeft:8,marginBottom:12,padding:4,borderRadius:4,border:'1px solid #cbd5e1'}}
      />
      {loading ? <div>Loading logs...</div> : (
        <ul style={{listStyle:'none',padding:0,maxHeight:350,overflowY:'auto'}}>
          {filteredLogs.map((entry, i) => (
            <li key={i} tabIndex={0} style={{marginBottom:8,background:'#fff',padding:10,borderRadius:6,boxShadow:'0 1px 2px #e2e8f0'}}>
              <pre style={{color:'#334155',fontSize:13}}>{JSON.stringify(entry, null, 2)}</pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
