import React, { useState } from "react";

export default function PartnerProgram() {
  const [status, setStatus] = useState("");
  const handleRegister = () => {
    setStatus("Partner registered (demo)");
    // TODO: Integrate with backend referral/affiliate logic
  };
  return (
    <div
      className="partner-program"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
      }}
    >
      <h2>Elite Partner & Affiliate Program</h2>
      <button
        onClick={handleRegister}
        style={{
          background: "#00e6ff",
          color: "#181e2b",
          border: "none",
          borderRadius: 8,
          padding: "8px 16px",
          fontWeight: "bold",
        }}
      >
        Register as Partner
      </button>
      {status && (
        <div style={{ marginTop: 16, color: "#00e6ff" }}>{status}</div>
      )}
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          Track referrals, earn commissions, and unlock white-label options.
          Owner-moderated and fully auditable.
        </em>
      </div>
    </div>
  );
}
