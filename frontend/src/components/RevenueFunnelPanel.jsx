import React, { useEffect, useState } from 'react';

// SAFE AI, deterministic, static, owner-controlled revenue funnel visualization
export default function RevenueFunnelPanel({ onAction }) {
  const [funnel, setFunnel] = useState({ stages: [], totals: {} });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/api/v110/revenue/funnel')
      .then(res => res.json())
      .then(data => {
        setFunnel(data);
        setError(null);
      })
      .catch(() => setError('Error loading revenue funnel'))
      .finally(() => setLoading(false));
  }, []);

  function handleExportCSV() {
    if (!funnel.stages.length) return;
    const csv = [
      'Stage,Count,Revenue',
      ...funnel.stages.map(s => `${s.name},${s.count},${s.revenue}`)
    ].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'revenue_funnel.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) return <div className="theme-card">Loading revenue funnel...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;

  return (
    <section aria-labelledby="revenue-funnel-heading" style={{background:'#fef9c3',borderRadius:14,padding:32,marginBottom:32,boxShadow:'0 2px 8px #fde68a'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h3 id="revenue-funnel-heading" style={{color:'#eab308',fontWeight:700,margin:0}}>Revenue Funnel</h3>
        <span style={{background:'#eab308',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="SAFE AI badge">SAFE AI</span>
        <span tabIndex={0} aria-label="Help: What is the Revenue Funnel?" title="Static, deterministic revenue funnel. OWNER controls all actions and exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <div style={{display:'flex',gap:32,alignItems:'flex-end',margin:'32px 0'}} aria-label="Revenue funnel visualization">
        {funnel.stages.map((stage, i) => (
          <div key={stage.name} style={{flex:1,textAlign:'center'}}>
            <div style={{height:40+stage.count*2,width:60,background:'#fde68a',borderRadius:10,margin:'0 auto',boxShadow:'0 1px 4px #eab30844',display:'flex',alignItems:'flex-end',justifyContent:'center'}} aria-label={`${stage.name} stage`}>
              <span style={{fontWeight:700,color:'#b45309'}}>{stage.count}</span>
            </div>
            <div style={{marginTop:8,fontWeight:600,color:'#b45309'}}>{stage.name}</div>
            <div style={{fontSize:13,color:'#a16207'}}>${stage.revenue}</div>
          </div>
        ))}
      </div>
      <div style={{marginTop:18,display:'flex',gap:16,alignItems:'center'}}>
        <button
          className="big-btn blue"
          aria-label="Export revenue funnel as CSV"
          title="Export revenue funnel as CSV (static, audit-logged)"
          onClick={handleExportCSV}
        >Export CSV</button>
        <button
          className="big-btn yellow"
          aria-label="Trigger funnel audit"
          title="Trigger static audit of revenue funnel (owner confirmation required, SAFE AI)"
          onClick={() => onAction && onAction('auditFunnel', { funnel })}
        >Audit Funnel</button>
      </div>
      <div style={{marginTop:16,color:'#a16207',fontSize:13}}>
        <b>OWNER CONTROLLED:</b> All actions require manual approval and are audit-logged. No adaptive or sentient logic.
      </div>
    </section>
  );
}
