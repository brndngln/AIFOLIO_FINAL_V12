import React, { useState, useEffect } from "react";

import Phase9RoleBadge from "./Phase9RoleBadge";
import Phase9AnalyticsPanel from "./Phase9AnalyticsPanel";

export default function Phase9KeyAdminPanel({ apiBase = "http://localhost:8090" }) {
  const [keys, setKeys] = useState({});
  const [keyMeta, setKeyMeta] = useState({}); // usage, last used, expiry, quota
  const [newKey, setNewKey] = useState("");
  const [newRole, setNewRole] = useState("viewer");
  const [bulkKeys, setBulkKeys] = useState("");
  const [bulkMode, setBulkMode] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showHelp, setShowHelp] = useState(false);
  const [editMetaKey, setEditMetaKey] = useState(null);
  const [editMeta, setEditMeta] = useState({expiry:'',quota:'',rotate:false});
  const [notify, setNotify] = useState(null);

  const fetchKeys = async () => {
    try {
      const res = await fetch(`${apiBase}/phase9/keys`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      });
      if (!res.ok) throw new Error("Failed to fetch keys");
      setKeys(await res.json());
      // fetch key meta (usage, last used, expiry, quota)
      const metaRes = await fetch(`${apiBase}/phase9/keys/meta`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}` }
      });
      if (metaRes.ok) setKeyMeta(await metaRes.json());
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

  const handleBulkImport = async () => {
    setError(null); setSuccess(null);
    try {
      const res = await fetch(`${apiBase}/phase9/keys/bulk_import`, {
        method: "POST",
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ keys: bulkKeys.split(/\r?\n/).map(l=>{
          const [key,role] = l.split(','); return {key:key.trim(),role:role?role.trim():'viewer'} }) })
      });
      if (!res.ok) throw new Error("Bulk import failed");
      setSuccess("Bulk import complete");
      setBulkKeys("");
      setBulkMode(false);
      fetchKeys();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleBulkExport = () => {
    const lines = Object.entries(keys).map(([k,r])=>`${k},${r}`);
    const blob = new Blob([lines.join('\n')],{type:'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'phase9_keys_export.txt'; a.click();
  };

  const handleEditMeta = (key) => {
    setEditMetaKey(key);
    setEditMeta({
      expiry: keyMeta[key]?.expiry||'',
      quota: keyMeta[key]?.quota||'',
      rotate: false
    });
  };

  const handleSaveMeta = async () => {
    setError(null); setSuccess(null);
    try {
      const res = await fetch(`${apiBase}/phase9/keys/meta/${editMetaKey}`, {
        method: "POST",
        headers: { 'Authorization': `Bearer ${localStorage.getItem('phase9_api_key') || ''}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(editMeta)
      });
      if (!res.ok) throw new Error("Failed to update key meta");
      setSuccess("Key meta updated");
      setEditMetaKey(null);
      fetchKeys();
    } catch(e) {
      setError(e.message);
    }
  };

  useEffect(() => {
    // Admin notifications: key expiring/overused
    let soon = Object.entries(keyMeta).filter(([k,m])=>m.expiry && new Date(m.expiry)-Date.now()<1000*60*60*24*7);
    let quota = Object.entries(keyMeta).filter(([k,m])=>m.quota && m.usage && m.usage>=m.quota);
    if(soon.length||quota.length) setNotify({soon,quota});
    else setNotify(null);
  }, [keyMeta]);

  // Determine if current user is admin (by API key in keys list)
  const apiKey = localStorage.getItem('phase9_api_key') || '';
  const userRole = keys[apiKey] || null;

  return (
    <div style={{border:'1px solid #bbb', borderRadius:8, padding:16, marginBottom:24, background:'#f9fafd'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h3 style={{marginBottom:8}}>Phase 9+ API Key Management</h3>
        <button onClick={()=>setShowHelp(true)} aria-label="Show help" title="Help">🛈</button>
      </div>
      {notify && (
        <div style={{background:'#fffbe6',color:'#b36a00',padding:8,borderRadius:5,marginBottom:10}}>
          {notify.soon.length>0 && <div>⚠️ Keys expiring soon: {notify.soon.map(([k])=>k).join(', ')}</div>}
          {notify.quota.length>0 && <div>⚠️ Keys over quota: {notify.quota.map(([k])=>k).join(', ')}</div>}
        </div>
      )}
      <div style={{marginBottom:12, display:'flex', alignItems:'center', gap:8, borderBottom:'1px solid #e6e6e6', paddingBottom:8}}>
        <input value={newKey} onChange={e => setNewKey(e.target.value)} placeholder="New API Key" style={{width:180}} />
        <select value={newRole} onChange={e => setNewRole(e.target.value)}>
          <option value="admin">admin</option>
          <option value="viewer">viewer</option>
          <option value="auditor">auditor</option>
          <option value="maintainer">maintainer</option>
          <option value="disabled">disabled</option>
        </select>
        <button onClick={handleAdd} disabled={!newKey || newRole === 'disabled'}>Add Key</button>
        <button onClick={()=>setBulkMode(b=>!b)}>{bulkMode?'Cancel Bulk':'Bulk Import/Export'}</button>
      </div>
      {bulkMode && (
        <div style={{marginBottom:12,background:'#f7f7fa',padding:8,borderRadius:5}}>
          <textarea value={bulkKeys} onChange={e=>setBulkKeys(e.target.value)} placeholder="key1,admin\nkey2,viewer" rows={3} style={{width:'100%',fontFamily:'monospace'}} />
          <div style={{marginTop:6}}>
            <button onClick={handleBulkImport} style={{marginRight:8}}>Import</button>
            <button onClick={handleBulkExport}>Export</button>
          </div>
        </div>
      )}
      <div style={{marginBottom:8}}>
        <b>Current Keys:</b>
        <ul style={{margin:0, paddingLeft:18}}>
          {Object.entries(keys).map(([k, r]) => (
            <li key={k} style={{marginBottom:4, display:'flex', alignItems:'center',gap:8,flexWrap:'wrap'}}>
              <span style={{fontFamily:'monospace'}}>{k}</span>
              <Phase9RoleBadge role={r} />
              <button onClick={() => handleRemove(k)} style={{marginLeft:8}} disabled={r === 'disabled'}>Remove</button>
              <button onClick={()=>handleEditMeta(k)} style={{marginLeft:8}}>Edit</button>
              {keyMeta[k] && (
                <span style={{fontSize:12,color:'#888',marginLeft:4}}>
                  Usage: {keyMeta[k].usage||0} | Last used: {keyMeta[k].last_used||'never'} | Expiry: {keyMeta[k].expiry||'none'} | Quota: {keyMeta[k].quota||'none'}
                </span>
              )}
            </li>
          ))}
        </ul>
      </div>
      {editMetaKey && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:10000}}>
          <div style={{background:'#fff',padding:24,borderRadius:8,minWidth:320}}>
            <h4>Edit Key Metadata</h4>
            <div style={{marginBottom:8}}>
              <label>Expiry: <input type="date" value={editMeta.expiry} onChange={e=>setEditMeta(m=>({...m,expiry:e.target.value}))} /></label>
            </div>
            <div style={{marginBottom:8}}>
              <label>Quota: <input type="number" value={editMeta.quota} onChange={e=>setEditMeta(m=>({...m,quota:e.target.value}))} /></label>
            </div>
            <div style={{marginBottom:8}}>
              <label><input type="checkbox" checked={editMeta.rotate} onChange={e=>setEditMeta(m=>({...m,rotate:e.target.checked}))} /> Rotate key</label>
            </div>
            <button onClick={handleSaveMeta} style={{marginRight:8}}>Save</button>
            <button onClick={()=>setEditMetaKey(null)}>Cancel</button>
          </div>
        </div>
      )}
      {showHelp && (
        <div role="dialog" aria-modal="true" style={{position:'fixed',top:0,left:0,right:0,bottom:0,background:'rgba(0,0,0,0.25)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:10000}}>
          <div style={{background:'#fff',padding:24,borderRadius:8,minWidth:320,maxWidth:600}}>
            <h4>Key Management Help</h4>
            <ul>
              <li>Add/remove keys and assign roles. All actions are logged for audit.</li>
              <li>Edit expiry and quotas, or rotate keys for compliance.</li>
              <li>Bulk import/export keys as CSV.</li>
              <li>Usage, last used, expiry, and quota are tracked for each key.</li>
              <li>Notifications for keys expiring soon or over quota.</li>
              <li>All features are admin-only and SAFE AI compliant.</li>
            </ul>
            <button onClick={()=>setShowHelp(false)}>Close</button>
          </div>
        </div>
      )}
      {error && <div style={{color:'red'}}>{error}</div>}
      {success && <div style={{color:'green'}}>{success}</div>}
    </div>
  );
}
