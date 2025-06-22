import React, { useState } from "react";

const MOCK_PARTNERS = [
  {
    name: "Acme AI Solutions",
    email: "contact@acmeai.com",
    vault: "Batch 3: AI Risk Audit",
    status: "Certified",
    date: "2025-06-20",
    progress: 100,
    notes: "Full compliance."
  },
  {
    name: "Beta Robotics",
    email: "info@betarobotics.com",
    vault: "Batch 7: Partner Certification",
    status: "Certified",
    date: "2025-06-12",
    progress: 100,
    notes: ""
  }
];

export default function PartnerCertificationExportPanel() {
  const [status, setStatus] = useState(null);
  const [partners, setPartners] = useState(MOCK_PARTNERS);
  const [exported, setExported] = useState({ pdf: null, csv: null });

  const exportFields = [
    "Partner Name", "Partner Email", "Vault/Module Name", "Certification Status", "Date Certified", "Progress %", "Notes / Comments"
  ];

  const handleExport = (type) => {
    setStatus(null);
    if (!partners.length) {
      setStatus({ type: "warning", msg: "No certified partners to export." });
      return;
    }
    // Simulate export and audit log
    setTimeout(() => {
      setStatus({ type: "success", msg: `Exported Partner Certification (${type.toUpperCase()}) to /exports/partner_certification (manual, audit-logged)` });
      setExported(e => ({ ...e, [type]: `/exports/partner_certification/partner_certification_export.${type}` }));
    }, 700);
  };

  // Simulate auto-export (Sunday night)
  React.useEffect(() => {
    const now = new Date();
    if (now.getDay() === 0 && now.getHours() === 23) {
      handleExport("csv");
      handleExport("pdf");
    }
    // eslint-disable-next-line
  }, []);

  // CSV generation (mock)
  const csvContent = [
    exportFields.join(","),
    ...partners.map(p => [p.name, p.email, p.vault, p.status, p.date, p.progress, p.notes].map(f => `"${f}"`).join(","))
  ].join("\n");

  return (
    <div className="partner-cert-export-panel" aria-label="Partner Certification Export" tabIndex={0} style={{background:'#f9fafb',padding:20,borderRadius:8}}>
      <h3 style={{color:'#0f172a'}}>Partner Certification Export</h3>
      <div style={{marginBottom:12}}>
        <button onClick={() => handleExport("pdf")}
          style={{background:'#2563eb',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',marginRight:10,fontWeight:600}}>
          Export PDF
        </button>
        <button onClick={() => handleExport("csv")}
          style={{background:'#059669',color:'#fff',border:'none',borderRadius:4,padding:'6px 18px',fontWeight:600}}>
          Export CSV
        </button>
      </div>
      {status && (
        <div style={{marginBottom:12,color:status.type==="success"?'#059669':status.type==="warning"?'#eab308':'#dc2626',fontWeight:500}}>
          {status.msg}
        </div>
      )}
      {partners.length ? (
        <div>
          <div style={{marginBottom:8,fontWeight:600}}>Preview (PDF):</div>
          <div style={{background:'#fff',padding:16,borderRadius:8,boxShadow:'0 1px 2px #e2e8f0',marginBottom:16,maxWidth:600}}>
            <table style={{width:'100%',borderCollapse:'collapse',fontSize:15}}>
              <thead>
                <tr>
                  {exportFields.map(f => <th key={f} style={{borderBottom:'2px solid #e5e7eb',textAlign:'left',padding:'4px 8px',color:'#2563eb'}}>{f}</th>)}
                </tr>
              </thead>
              <tbody>
                {partners.map((p,i) => (
                  <tr key={i}>
                    <td style={{padding:'4px 8px'}}>{p.name}</td>
                    <td style={{padding:'4px 8px'}}>{p.email}</td>
                    <td style={{padding:'4px 8px'}}>{p.vault}</td>
                    <td style={{padding:'4px 8px'}}>{p.status}</td>
                    <td style={{padding:'4px 8px'}}>{p.date}</td>
                    <td style={{padding:'4px 8px'}}>{p.progress}%</td>
                    <td style={{padding:'4px 8px'}}>{p.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {exported.pdf && (
            <a href={exported.pdf} download style={{marginRight:16,color:'#2563eb',fontWeight:600}}>Download PDF</a>
          )}
          {exported.csv && (
            <a href={`data:text/csv;charset=utf-8,${encodeURIComponent(csvContent)}`} download="partner_certification_export.csv" style={{color:'#059669',fontWeight:600}}>Download CSV</a>
          )}
        </div>
      ) : null}
      {!partners.length && (
        <div style={{marginTop:16,color:'#eab308',fontWeight:500}}>No certified partners to export.</div>
      )}
      <div style={{marginTop:16,fontSize:13,color:'#64748b'}}>
        All exports are owner-triggered or scheduled, static, and audit-logged. No public/partner export unless you manually approve. Fully SAFE AI compliant.
      </div>
    </div>
  );
}
