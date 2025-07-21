// ApiKeyStatus.jsx
// SAFE AI static API key status indicator for Muse Haven
import React from "react";

export default function ApiKeyStatus() {
  const [status, setStatus] = React.useState(null);
  React.useEffect(() => {
    fetch("/api/api-keys", { credentials: "include" })
      .then((r) => (r.ok ? r.json() : {}))
      .then(setStatus);
  }, []);
  if (!status) return <span style={{ color: "#aaa" }}>Loading...</span>;
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
      {Object.entries(status).map(([k, v]) => (
        <li
          key={k}
          style={{
            color: v === "present" ? "#4cafef" : "#f44336",
            fontWeight: v === "present" ? "bold" : "normal",
          }}
        >
          {k}: {v}
        </li>
      ))}
    </ul>
  );
}
