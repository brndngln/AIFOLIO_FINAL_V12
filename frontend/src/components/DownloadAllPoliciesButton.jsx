import React from "react";

export default function DownloadAllPoliciesButton() {
  // This implementation triggers download of all policy docs as a zip (static sample)
  const handleDownload = () => {
    // In a real static app, you would link to a pre-zipped file or trigger multiple downloads
    window.open('/src/policy/TermsOfService.md', '_blank');
    window.open('/src/policy/RefundPolicy.md', '_blank');
    window.open('/src/policy/PrivacyPolicy.md', '_blank');
  };
  return (
    <button
      style={{background:'#0ea5e9',color:'#fff',border:'none',borderRadius:6,padding:'10px 20px',fontWeight:700,fontSize:15,cursor:'pointer',marginBottom:16,marginTop:8,boxShadow:'0 1px 2px #bae6fd'}}
      aria-label="Download all policy documents"
      onClick={handleDownload}
    >
      Download All Policies
    </button>
  );
}
