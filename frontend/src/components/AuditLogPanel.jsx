import React from "react";
export default function AuditLogPanel({ auditLog }) {
  return (
    <div style={{marginTop:32, background:'#fff', borderRadius:8, padding:20, boxShadow:'0 1px 3px #e5e7eb'}}>
      <h3 style={{color:'#334155', fontWeight:600, marginBottom:8}}>Audit Log</h3>
      <ul style={{listStyle:'none', padding:0, fontSize:13, maxHeight:200, overflowY:'auto'}}>
        {auditLog.length === 0 && <li style={{color:'#64748b'}}>No actions logged yet.</li>}
        {auditLog.map((entry, i) => (
          <li key={i} style={{marginBottom:6}}>
            <span style={{color:'#2563eb', fontWeight:500}}>{entry.time}:</span> {entry.action} ({entry.status})
          </li>
        ))}
      </ul>
    </div>
  );
}
