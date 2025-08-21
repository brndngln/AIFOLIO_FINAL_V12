import React from "react";

export default function OwnerGuide() {
  return (
    <div
      className="owner-guide"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
        maxWidth: 700,
        margin: "0 auto",
      }}
    >
      <h2>Dynamic Owner/Operator Guide</h2>
      <ul style={{ lineHeight: 2 }}>
        <li>
          <strong>SAFE AI Compliance:</strong> All modules are deterministic,
          static, and owner-controlled.
        </li>
        <li>
          <strong>Audit & Compliance Dashboard:</strong> Monitor, export, and
          review all audit trails.
        </li>
        <li>
          <strong>Prompt Marketplace:</strong> Submit, review, and monetize
          prompt sets.
        </li>
        <li>
          <strong>Workflow Builder:</strong> Create and manage multi-step prompt
          flows.
        </li>
        <li>
          <strong>Export Panel:</strong> Export branded, licensing-ready
          deliverables in multiple formats.
        </li>
        <li>
          <strong>Automation Builder:</strong> Connect vault events to external
          services.
        </li>
        <li>
          <strong>Billing & Partner Program:</strong> Manage subscriptions,
          partners, and affiliate programs.
        </li>
        <li>
          <strong>Leaderboard:</strong> Track vault usage, exports, and
          community contributions.
        </li>
        <li>
          <strong>AI Override & Redaction:</strong> Owner can approve/edit AI
          output and redact sensitive data.
        </li>
        <li>
          <strong>Backup & Recovery:</strong> Create, restore, and manage
          versioned backups.
        </li>
      </ul>
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          This guide auto-updates as new features are deployed. You are always
          in full control of your elite AIFOLIO business.
        </em>
      </div>
    </div>
  );
}
