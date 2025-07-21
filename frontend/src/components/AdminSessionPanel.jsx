import React from "react";
import HyperEliteVaultBadge from "../../components/HyperEliteVaultBadge";

// This is a static, deterministic session viewer for SAFE AI compliance.
const STATIC_SESSIONS = [
  {
    user: "admin",
    role: "admin",
    loginTime: "2025-06-22T16:55:00-06:00",
    sessionId: "sess-001",
  },
  {
    user: "partner1",
    role: "partner",
    loginTime: "2025-06-22T16:45:00-06:00",
    sessionId: "sess-002",
  },
];

export default function AdminSessionPanel() {
  return (
    <div
      className="admin-session-panel"
      aria-label="Admin Sessions"
      tabIndex={0}
      style={{ background: "#f9fafb", padding: 20, borderRadius: 8 }}
    >
      <h3
        style={{
          color: "#0f172a",
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        Active Sessions (Static Example)
        <HyperEliteVaultBadge tooltip={true} external={false} />
      </h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {STATIC_SESSIONS.map((sess) => (
          <li
            key={sess.sessionId}
            style={{
              marginBottom: 8,
              background: "#fff",
              padding: 10,
              borderRadius: 6,
              boxShadow: "0 1px 2px #e2e8f0",
            }}
          >
            <b>User:</b> {sess.user} ({sess.role})<br />
            <b>Login Time:</b> {sess.loginTime}
            <br />
            <b>Session ID:</b> {sess.sessionId}
          </li>
        ))}
      </ul>
    </div>
  );
}
