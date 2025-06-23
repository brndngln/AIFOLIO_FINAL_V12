import React from "react";

export default function OwnerManualPriceLockPanel() {
  return (
    <section aria-labelledby="manual-price-lock-heading" style={{background:'#f1f5f9',borderRadius:12,padding:24,marginBottom:24,boxShadow:'0 1px 4px #dbeafe'}}>
      <h3 id="manual-price-lock-heading" style={{color:'#0ea5e9',fontWeight:700,marginBottom:10}}>Manual Price Lock</h3>
      <p style={{fontSize:15,marginBottom:12}}>OWNER can set and lock the price for any vault. All pricing is static, deterministic, and audit-logged. No adaptive/AI pricing.</p>
      <input
        type="number"
        min="1"
        step="0.01"
        aria-label="Set manual price"
        placeholder="Enter price (USD)"
        style={{padding:8,borderRadius:6,border:'1px solid #cbd5e1',marginRight:8,fontSize:15}}
      />
      <button
        style={{background:'#0ea5e9',color:'#fff',border:'none',borderRadius:6,padding:'8px 16px',fontWeight:700,fontSize:15,cursor:'pointer'}}
        aria-label="Lock price"
        onClick={()=>alert('Price locked (static, OWNER-controlled).')}
      >
        Lock Price
      </button>
      <div style={{marginTop:10,color:'#64748b',fontSize:13}}>
        All price changes are OWNER-controlled and statically audit-logged.
      </div>
    </section>
  );
}
