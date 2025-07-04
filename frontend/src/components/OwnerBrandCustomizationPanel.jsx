import React, { useState } from "react";

const DEFAULTS = {
  name: "AIFOLIO",
  logo: "/logo192.png",
  color: "#0ea5e9"
};

<<<<<<< HEAD
=======
// [WINDSURF FIXED ✅]
>>>>>>> omni_repair_backup_20250704_1335
export default function OwnerBrandCustomizationPanel() {
  const [brand, setBrand] = useState(() => {
    const saved = localStorage.getItem("aifolio_brand");
    return saved ? JSON.parse(saved) : DEFAULTS;
<<<<<<< HEAD
  });
=======
  }); // Remove if not used in render or logic
>>>>>>> omni_repair_backup_20250704_1335

  function handleChange(e) {
    const { name, value } = e.target;
    const next = { ...brand, [name]: value };
    setBrand(next);
    localStorage.setItem("aifolio_brand", JSON.stringify(next));
  }

  return (
    <section aria-labelledby="brand-customization-heading" style={{background:'#f9fafb',borderRadius:12,padding:32,marginBottom:32,boxShadow:'0 2px 8px #e0e7ef'}}>
      <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:12}}>
        <h2 id="brand-customization-heading" style={{color:'#0ea5e9',fontWeight:800,fontSize:22,margin:0}}>OWNER Brand Customization</h2>
        <span style={{background:'#0ea5e9',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="OWNER badge">OWNER</span>
        <span tabIndex={0} aria-label="Help: Brand customization" title="Change your business name, logo, and highlight color. Static preview only." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </div>
      <form style={{display:'flex',flexDirection:'column',gap:16,maxWidth:380}} aria-label="Brand customization form">
        <label style={{fontWeight:600}}>
          AIFOLIO Name
          <input
            type="text"
            name="name"
            value={brand.name}
            onChange={handleChange}
            style={{width:'100%',padding:8,borderRadius:6,border:'1px solid #e5e7eb',marginTop:4}}
            aria-label="AIFOLIO name"
          />
        </label>
        <label style={{fontWeight:600}}>
          Logo URL
          <input
            type="text"
            name="logo"
            value={brand.logo}
            onChange={handleChange}
            style={{width:'100%',padding:8,borderRadius:6,border:'1px solid #e5e7eb',marginTop:4}}
            aria-label="Logo URL"
          />
        </label>
        <label style={{fontWeight:600}}>
          Highlight Color
          <input
            type="color"
            name="color"
            value={brand.color}
            onChange={handleChange}
            style={{width:48,height:32,border:'none',marginTop:4}}
            aria-label="Highlight color"
          />
        </label>
      </form>
      <div style={{marginTop:24,padding:16,background:'#fff',border:'1px solid #e5e7eb',borderRadius:8}}>
        <b>Preview:</b>
        <div style={{display:'flex',alignItems:'center',gap:16,marginTop:12}}>
          <img src={brand.logo} alt="Logo preview" style={{width:48,height:48,borderRadius:8,background:'#f1f5f9',border:'1px solid #e5e7eb'}} />
          <span style={{fontWeight:700,fontSize:19,color:brand.color}}>{brand.name}</span>
        </div>
      </div>
      <div style={{marginTop:18,color:'#64748b',fontSize:13}}>
        <b>OWNER CONTROLLED:</b> Brand settings are saved in your browser only. No backend or adaptive logic.
      </div>
    </section>
  );
}
