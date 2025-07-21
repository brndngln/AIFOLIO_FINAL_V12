import React from "react";

export default function SafeguardValidationLayer() {
  return (
    <div
      style={{
        marginTop: 32,
        background: "#f9fafb",
        borderRadius: 8,
        padding: 24,
        boxShadow: "0 1px 3px #e5e7eb",
      }}
    >
      <h3 style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 12 }}>
        SAFEGUARD & VALIDATION LAYER
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        <li>✔️ Automation Test Vault</li>
        <li>✔️ Metadata Validator</li>
        <li>✔️ Preview Enforcement</li>
        <li>✔️ Secure PDF Delivery</li>
        <li>✔️ Stripe/Gumroad Payment Checks</li>
        <li>✔️ Smart Pricing Checks</li>
        <li>✔️ Bot Upload Sanity Checks</li>
        <li>✔️ Beginner mistake prevention</li>
      </ul>
    </div>
  );
}
