import React, { useState, useEffect } from "react";

export default function Phase9KeyAdminPanel({ apiBase = "http://localhost:8090" }) {
  const [keys, setKeys] = useState({});
  const [newKey, setNewKey] = useState("");
  const [newRole, setNewRole] = useState("viewer");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const fetchKeys = async () => {
    try {
      const res = await fetch(`${apiBase}/phase9/keys`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      });
      if (!res.ok) throw new Error("Failed to fetch keys");
      setKeys(await res.json());
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => { fetchKeys(); }, []);

  const handleAdd = async () => {
    setError(null); setSuccess(null);
    try {
      const res = await fetch(`${apiBase}/phase9/keys`, {
        method: "POST",
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: newKey, role: newRole })
      });
      if (!res.ok) throw new Error("Failed to add key");
      setSuccess("Key added");
      setNewKey("");
      fetchKeys();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleRemove = async (key) => {
    setError(null); setSuccess(null);
    try {
      const res = await fetch(`${apiBase}/phase9/keys/${key}`, {
        method: "DELETE",
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      });
      if (!res.ok) throw new Error("Failed to remove key");
      setSuccess("Key removed");
      fetchKeys();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={{border:'1px solid #bbb', borderRadius:8, padding:16, marginBottom:24, background:'#f9fafd'}}>
      <h3>Phase 9+ API Key Management</h3>
      <div style={{marginBottom:12}}>
        <input value={newKey} onChange={e => setNewKey(e.target.value)} placeholder="New API Key" style={{width:180,marginRight:8}} />
        <select value={newRole} onChange={e => setNewRole(e.target.value)}>
          <option value="admin">admin</option>
          <option value="viewer">viewer</option>
        </select>
        <button onClick={handleAdd} disabled={!newKey}>Add Key</button>
      </div>
      <div style={{marginBottom:8}}>
        <b>Current Keys:</b>
        <ul style={{margin:0, paddingLeft:18}}>
          {Object.entries(keys).map(([k, r]) => (
            <li key={k} style={{marginBottom:4}}>
              <span style={{fontFamily:'monospace'}}>{k}</span> ({r})
              <button onClick={() => handleRemove(k)} style={{marginLeft:8}}>Remove</button>
            </li>
          ))}
        </ul>
      </div>
      {error && <div style={{color:'red'}}>{error}</div>}
      {success && <div style={{color:'green'}}>{success}</div>}
    </div>
  );
}
