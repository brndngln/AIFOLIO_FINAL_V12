import React from "react";

export default function SupportPanel() {
  return (
    <section
      aria-labelledby="support-heading"
      style={{
        background: "#f0fdfa",
        borderRadius: 12,
        padding: 24,
        marginBottom: 24,
        boxShadow: "0 1px 4px #bae6fd",
      }}
    >
      <h3
        id="support-heading"
        style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 10 }}
      >
        Support & Contact
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        <li>
          Email:{" "}
          <a
            href="mailto:owner@aifolio.com"
            style={{ color: "#0ea5e9", textDecoration: "underline" }}
          >
            owner@aifolio.com
          </a>
        </li>
        <li>GDPR Requests: Use the static GDPR dashboard or email above</li>
        <li></li>
      </ul>
    </section>
  );
}
