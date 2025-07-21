import React from "react";

const LockdownMode = () => (
  <div
    style={{
      minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      background: "#212121",
      color: "#e5d6b2",
      fontFamily: "Montserrat, Arial, sans-serif",
      textAlign: "center",
      letterSpacing: "0.03em",
      padding: "0 24px",
    }}
  >
    <h1 style={{ fontSize: "2.5rem", marginBottom: 24 }}>
      Security Protocol Engaged
    </h1>
    <p style={{ fontSize: "1.25rem", maxWidth: 520, marginBottom: 32 }}>
      <b>Vault Reset in Progress.</b>
      <br />
      All key-dependent services are halted.
      <br />
      Please contact the system owner or security administrator.
      <br />
      <br />
      <span style={{ color: "#ff5252", fontWeight: 600 }}>
        AIFOLIO™ is in Lockdown Mode.
      </span>
    </p>
    <div style={{ marginTop: 40, fontSize: 18, color: "#ff5252" }}>
      <span role="img" aria-label="lock">
        🔒
      </span>{" "}
      <b>All access is temporarily restricted.</b>
    </div>
  </div>
);

export default LockdownMode;
