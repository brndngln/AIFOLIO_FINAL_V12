// OnboardingOverlay.jsx
// Muse Haven onboarding/tutorial overlay component
import React from "react";

export default function OnboardingOverlay({ step, onNext, onClose }) {
  const steps = [
    "Welcome to Muse Haven! This is your private, owner-exclusive sanctuary.",
    "Access is protected by secret triggers and multi-factor authentication.",
    "Customize Emma’s appearance, persona, and preferences in the Customization dashboard.",
    "Adjust learning mode and feedback for fully owner-controlled, SAFE AI-compliant adaptation.",
    "All chats, content, and preferences are stored in a quantum-encrypted, owner-only vault.",
    "Trigger emergency lockdown at any time for instant purge and lockout.",
    "Access contextual help via the (?) buttons throughout the portal.",
    "Use the ⚙️ Owner Control Center (top left) for all integrations, notification toggles, API key rotation, compliance audit, and logs.",
    "Integrations: Toggle Slack, Discord, and Email notifications for owner events.",
    "Integrations are static and SAFE AI-compliant: notifications are owner-controlled and never expose data.",
    "API Key Rotation: Instantly rotate all API keys (static, owner-only, SAFE AI-compliant).",
    "Compliance Audit: Run/export static compliance audit for SAFE AI, privacy, and security.",
    "Compliance audit is fully deterministic and logged; no secrets or adaptive logic.",
    "API Key Status: Instantly see if required integrations are set up—no secrets ever shown.",
    "Accessibility: Full keyboard navigation, ARIA labels, high-contrast, and large touch targets.",
    'Need help? Launch this onboarding anytime (bottom left ?) or click any "?" for contextual help. FAQ and troubleshooting are in the README.',
    "Configure notification preferences in the Owner Control Center.",
    "Rotate API keys for enhanced security.",
    "Run a compliance audit to ensure SAFE AI and regulatory compliance.",
  ];
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        background: "rgba(0,0,0,0.8)",
        zIndex: 9999,
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
      aria-modal="true"
      role="dialog"
    >
      <div
        style={{
          maxWidth: 500,
          padding: 30,
          background: "#222",
          borderRadius: 18,
          boxShadow: "0 8px 32px rgba(0,0,0,0.25)",
        }}
      >
        <h3 style={{ marginBottom: 8 }}>Onboarding</h3>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: 16,
          }}
          aria-label="Onboarding Progress"
        >
          {steps.map((_, i) => (
            <div
              key={i}
              style={{
                width: 12,
                height: 12,
                borderRadius: "50%",
                margin: "0 4px",
                background: i === step ? "#fff" : "#555",
                border: i === step ? "2px solid #4cafef" : "2px solid #222",
              }}
            ></div>
          ))}
        </div>
        <p style={{ fontSize: 18, lineHeight: 1.5 }}>{steps[step]}</p>
        <div
          style={{ marginTop: 24, display: "flex", justifyContent: "center" }}
        >
          {step < steps.length - 1 ? (
            <button
              onClick={onNext}
              style={{
                fontSize: 18,
                padding: "12px 32px",
                borderRadius: 8,
                background: "#4cafef",
                color: "#fff",
                border: "none",
                boxShadow: "0 2px 8px #222",
                cursor: "pointer",
              }}
            >
              Next
            </button>
          ) : (
            <button
              onClick={onClose}
              style={{
                fontSize: 18,
                padding: "12px 32px",
                borderRadius: 8,
                background: "#22c55e",
                color: "#fff",
                border: "none",
                boxShadow: "0 2px 8px #222",
                cursor: "pointer",
              }}
            >
              Finish
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
