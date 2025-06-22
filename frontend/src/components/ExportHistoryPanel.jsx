import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ExportHistoryPanel({ token }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userFilter, setUserFilter] = useState("");

  useEffect(() => {
    setLoading(true);
    axios.get("/admin/export-history", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => setHistory(res.data))
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, [token]);

  const filteredHistory = userFilter
    ? history.filter(entry => entry.user && entry.user.includes(userFilter))
    : history;

  return (
    <div className="export-history-panel" aria-label="Export History" tabIndex={0} style={{background:'#f1f5f9',padding:20,borderRadius:8}}>
      <h3 style={{color:'#0f172a'}}>Export/Download History</h3>
      <label htmlFor="user-filter-export" style={{fontWeight:600}}>Filter by user:</label>
      <input
        id="user-filter-export"
        aria-label="Filter by user"
        value={userFilter}
        onChange={e => setUserFilter(e.target.value)}
        style={{marginLeft:8,marginBottom:12,padding:4,borderRadius:4,border:'1px solid #cbd5e1'}}
      />
      {loading ? <div>Loading history...</div> : (
        <ul style={{listStyle:'none',padding:0,maxHeight:350,overflowY:'auto'}}>
          {filteredHistory.map((entry, i) => (
            <li key={i} tabIndex={0} style={{marginBottom:8,background:'#fff',padding:10,borderRadius:6,boxShadow:'0 1px 2px #e2e8f0'}}>
              <pre style={{color:'#334155',fontSize:13}}>{JSON.stringify(entry, null, 2)}</pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
