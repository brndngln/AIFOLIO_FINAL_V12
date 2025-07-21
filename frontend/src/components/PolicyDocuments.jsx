import React, { useState } from "react";

const policies = [
  {
    title: "Terms of Service",
    summary: "Static, system-focused terms for all users.",
    content: `# Terms of Service\n\nWelcome to AIFOLIO. By using this service, you agree to the following terms:\n\n1. **System Use Only:** The system is for authorized system use only.\n2. **No Public/Global/NGO Use:** No public, global, or NGO use is permitted.\n3. **PDF Vaults:** All products are digital PDF vaults, delivered securely.\n4. **No Liability:** AIFOLIO is not liable for system losses, data loss, or indirect damages.\n5. **Compliance:** You agree to comply with all local, national, and international laws applicable to your system use.\n6. **Audit Logging:** All actions are audit-logged for compliance and security.\n7. **OWNER Control:** All exports and outputs require explicit OWNER approval.\n8. **No Auto-Publishing:** No content is auto-published. All outputs are static, deterministic, and OWNER-controlled.\n\nBy continuing to use AIFOLIO, you acknowledge and accept these terms.`,
  },
  {
    title: "Refund Policy",
    summary: "Clear refund terms for digital vaults.",
    content: `# Refund Policy\n\nAIFOLIO offers digital PDF vault products. Refunds are available under the following conditions:\n\n- **Duplicate Purchase:** If you accidentally purchase the same vault twice, contact support for a refund.\n- **Corrupt File:** If your PDF vault is corrupt or fails to open, contact support within 7 days for a replacement or refund.\n- **Non-Delivery:** If you do not receive your vault within 24 hours, contact support for assistance.\n- **No Refunds for Downloaded Vaults:** Once a vault has been successfully downloaded and accessed, no refunds are provided except as required by law.\n\nAll refund requests are subject to OWNER review and audit log verification.`,
  },
  {
    title: "Privacy Policy",
    summary: "GDPR/CCPA compliant, static privacy statement.",
    content: `# Privacy Policy\n\nAIFOLIO is committed to protecting your privacy and complying with GDPR/CCPA. Our privacy principles:\n\n- **No Personal Tracking:** We do not track or sell personal data. Only aggregate, non-personal analytics are collected.\n- **Audit Logging:** All actions are logged for compliance and security.\n- **Opt-Out:** Users may request data access or deletion at any time via the GDPR Request Dashboard.\n- **Data Retention:** Only essential business and compliance data is retained. No unnecessary retention.\n- **No Third-Party Marketing:** No user data is shared with third-party marketers.\n\nFor privacy requests, contact OWNER or use the static GDPR dashboard.`,
  },
];

import DownloadAllPoliciesButton from "./DownloadAllPoliciesButton";

export default function PolicyDocuments() {
  const [open, setOpen] = useState([false, false, false]); // Remove if not used in render or logic
  return (
    <div
      style={{
        marginTop: 32,
        background: "#fff",
        borderRadius: 8,
        padding: 24,
        boxShadow: "0 1px 3px #e5e7eb",
      }}
    >
      <h3 style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 12 }}>
        POLICY DOCUMENTS
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        {policies.map((policy, i) => (
          <li key={policy.title} style={{ marginBottom: 16 }}>
            <button
              style={{
                background: "none",
                border: "none",
                color: "#0ea5e9",
                fontWeight: 600,
                fontSize: 16,
                cursor: "pointer",
                padding: 0,
                textAlign: "left",
              }}
              onClick={() =>
                setOpen((open) => open.map((o, idx) => (idx === i ? !o : o)))
              }
              aria-expanded={open[i]}
              aria-controls={`policy-content-${i}`}
            >
              {open[i] ? "▼" : "▶"} {policy.title}
            </button>
            <div style={{ marginLeft: 24, marginTop: 4 }}>
              {!open[i] && (
                <span style={{ color: "#64748b", fontSize: 14 }}>
                  {policy.summary}
                </span>
              )}
              {open[i] && (
                <pre
                  id={`policy-content-${i}`}
                  style={{
                    whiteSpace: "pre-wrap",
                    background: "#f3f4f6",
                    padding: 12,
                    borderRadius: 6,
                    marginTop: 8,
                    fontSize: 14,
                  }}
                >
                  {policy.content}
                </pre>
              )}
            </div>
          </li>
        ))}
      </ul>
      <DownloadAllPoliciesButton />
    </div>
  );
}
