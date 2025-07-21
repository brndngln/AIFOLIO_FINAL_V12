import React from "react";

const MISTAKES = [
  "Skipping preview check",
  "Publishing without testing vault",
  "Using public Google Drive links",
  "Missing payout setup",
  "Skipping webhook for PDF delivery",
  "Broken metadata",
  "Auto-publish unverified vaults",
  "Forgetting GDPR opt-outs",
  "Not running Final Completion Checklist",
  "Forgetting UX Best Practices",
];

export default function BeginnerMistakesToAvoid() {
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
      <h3 style={{ color: "#ef4444", fontWeight: 700, marginBottom: 12 }}>
        Beginner Mistakes to Avoid
      </h3>
      <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
        {MISTAKES.map((item, i) => (
          <li key={i} style={{ marginBottom: 8 }}>
            <span style={{ color: "#ef4444", fontWeight: 600 }}>✘</span> {item}
          </li>
        ))}
      </ul>
      <div style={{ marginTop: 18, color: "#64748b", fontSize: 13 }}>
        <b>OWNER CONTROLLED:</b> Avoid all above mistakes to maintain SAFE AI
        compliance and trust.
      </div>
    </div>
  );
}
