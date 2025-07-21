import React from "react";

const FAQ = [
  { q: "What is AIFOLIO?", a: "A secure, OWNER-controlled PDF vault system." },
  {
    q: "Is this app adaptive or AI-driven?",
    a: "No, it is fully static, deterministic, and non-adaptive.",
  },
  {
    q: "How do I install as a PWA?",
    a: "Open in your browser, click 'Add to Home Screen', and follow prompts.",
  },
  {
    q: "How do I request a refund?",
    a: "See the Refund Policy in the Policy Documents panel.",
  },
  {
    q: "How do I contact support?",
    a: "Email owner@aifolio.com or use the Support panel.",
  },
  {
    q: "How do I export all policy docs?",
    a: "Use the 'Download All Policies' button in the Policy Documents panel.",
  },
];

export default function FAQPanel() {
  return (
    <section
      aria-labelledby="faq-heading"
      style={{
        background: "#f3f4f6",
        borderRadius: 12,
        padding: 24,
        marginBottom: 24,
        boxShadow: "0 1px 4px #cbd5e1",
      }}
    >
      <h3
        id="faq-heading"
        style={{ color: "#0ea5e9", fontWeight: 700, marginBottom: 10 }}
      >
        Frequently Asked Questions
      </h3>
      <ul style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}>
        {FAQ.map((item, i) => (
          <li key={i} style={{ marginBottom: 8 }}>
            <b>Q:</b> {item.q}
            <br />
            <span style={{ color: "#64748b" }}>A: {item.a}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
