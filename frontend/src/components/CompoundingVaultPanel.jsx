import React, { useEffect, useState } from 'react';
<<<<<<< HEAD

// SAFE AI, deterministic, static, owner-controlled compounding vault controls
export default function CompoundingVaultPanel({ onAction }) {
=======
import PropTypes from 'prop-types';

// SAFE AI, deterministic, static, owner-controlled compounding vault controls
function CompoundingVaultPanel({ onAction }) {
>>>>>>> omni_repair_backup_20250704_1335
  const [vaults, setVaults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/api/v110/vaults/compounding')
      .then(res => res.json())
      .then(data => {
        setVaults(data.vaults || []);
        setError(null);
      })
      .catch(() => setError('Error loading compounding vaults'))
      .finally(() => setLoading(false));
  }, []);

  function handleExportCSV() {
    if (!vaults.length) return;
    const csv = [
      'Vault,Status,Principal,Interest,Compounded',
      ...vaults.map(v => `${v.name},${v.status},${v.principal},${v.interest},${v.compounded}`)
    ].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compounding_vaults.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) return <div className="theme-card">Loading compounding vaults...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;

  return (
    <section aria-labelledby="compounding-vault-heading" style={{background:'#fef9c3',borderRadius:14,padding:32,marginBottom:32,boxShadow:'0 2px 8px #fde68a'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h3 id="compounding-vault-heading" style={{color:'#eab308',fontWeight:700,margin:0}}>Compounding Vault Controls</h3>
        <span style={{background:'#eab308',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="SAFE AI badge">SAFE AI</span>
        <span tabIndex={0} aria-label="Help: What are Compounding Vaults?" title="Static, deterministic compounding vault controls. OWNER controls all actions and exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <table aria-label="Compounding vaults list" style={{width:'100%',marginBottom:18,background:'#fff',borderRadius:8,boxShadow:'0 1px 2px #e5e7eb'}}>
        <thead>
          <tr style={{background:'#e0e7ef'}}>
            <th>Vault</th>
            <th>Status</th>
            <th>Principal</th>
            <th>Interest</th>
            <th>Compounded</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {vaults.map((v, i) => (
            <tr key={i}>
              <td>{v.name}</td>
              <td>{v.status}</td>
              <td>${v.principal}</td>
              <td>${v.interest}</td>
              <td>${v.compounded}</td>
              <td>
                <button
                  className="big-btn yellow"
                  aria-label={`Audit compounding vault ${v.name}`}
                  title="Audit this compounding vault (owner confirmation required, SAFE AI)"
                  onClick={() => onAction && onAction('auditCompoundingVault', { vault: v })}
                >Audit</button>
                <button
                  className="big-btn blue"
                  aria-label={`Export compounding vault ${v.name} as CSV`}
                  title="Export this compounding vault as CSV (static, audit-logged)"
                  onClick={() => {
                    const csv = `Vault,Status,Principal,Interest,Compounded\n${v.name},${v.status},${v.principal},${v.interest},${v.compounded}`;
                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `compounding_vault_${v.name}.csv`;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                >Export</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{marginTop:18,display:'flex',gap:16,alignItems:'center'}}>
        <button
          className="big-btn blue"
          aria-label="Export all compounding vaults as CSV"
          title="Export all compounding vaults as CSV (static, audit-logged)"
          onClick={handleExportCSV}
        >Export All CSV</button>
        <button
          className="big-btn yellow"
          aria-label="Trigger compounding vault audit"
          title="Trigger static audit of compounding vaults (owner confirmation required, SAFE AI)"
          onClick={() => onAction && onAction('auditAllCompoundingVaults', { vaults })}
        >Audit All</button>
      </div>
      <div style={{marginTop:16,color:'#a16207',fontSize:13}}>
        <b>OWNER CONTROLLED:</b> All actions require manual approval and are audit-logged. No adaptive or sentient logic.
      </div>
    </section>
  );
}
<<<<<<< HEAD
=======

CompoundingVaultPanel.propTypes = {
  onAction: PropTypes.func
}; // [WINDSURF FIXED]

export default CompoundingVaultPanel; // [WINDSURF FIXED]

>>>>>>> omni_repair_backup_20250704_1335
