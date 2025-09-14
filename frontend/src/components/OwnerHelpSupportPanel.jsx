import React from "react";

const FAQ = [
  {
    q: "How do I edit my business info?",
    a: "Go to the Brand Customization panel to update your name, logo, and colors.",
  },
  {
    q: "How do I export all my data?",
    a: "Use the Export All Data panel to select and download your business data as a ZIP.",
  },
  {
    q: "How do I install as a PWA?",
    a: "In Chrome or Safari, use the browser menu to add AIFOLIO to your Home Screen or Desktop.",
  },
  {
    q: "How do I update policy docs?",
    a: "Edit the markdown files in the Policy section, then export or print as needed.",
  },
  {
    q: "How do I get support?",
    a: "See the support contact below or use the static support request template.",
  },
];

export default function OwnerHelpSupportPanel() {
  return (
    <section
      aria-labelledby="owner-help-heading"
      style={{
        background: "#f9fafb",
        borderRadius: 12,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #e0e7ef",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginBottom: 12,
        }}
      >
        <h2
          id="owner-help-heading"
          style={{ color: "#0ea5e9", fontWeight: 800, fontSize: 22, margin: 0 }}
        >
          OWNER Help & Support
        </h2>
        <span
          style={{
            background: "#0ea5e9",
            color: "#fff",
            padding: "2px 10px",
            borderRadius: 6,
            fontWeight: 700,
            fontSize: 13,
          }}
          aria-label="OWNER badge"
        >
          OWNER
        </span>
        <span
          tabIndex={0}
          aria-label="Help: OWNER support"
          title="Find answers, support, and contact info for OWNER users."
          style={{
            marginLeft: 6,
            color: "#64748b",
            cursor: "help",
            fontSize: 18,
            fontWeight: 800,
          }}
        >
          ?
        </span>
      </div>
      <ul
        style={{ listStyle: "none", padding: 0, fontSize: 15 }}
        aria-label="OWNER FAQ"
      >
        {FAQ.map((item, i) => (
          <li key={i} style={{ marginBottom: 16 }}>
            <b style={{ color: "#0ea5e9" }}>Q:</b>{" "}
            <span tabIndex={0} aria-label={`FAQ question: ${item.q}`}>
              {item.q}
            </span>
            <br />
            <span
              style={{ color: "#64748b", marginLeft: 24 }}
              tabIndex={0}
              aria-label={`FAQ answer: ${item.a}`}
            >
              {item.a}
            </span>
          </li>
        ))}
      </ul>
      <div style={{ marginTop: 18, color: "#64748b", fontSize: 13 }}>
        <b>Support Contact:</b>{" "}
        <span aria-label="Support email">user@example.com</span>
        <br />
        <b>Static Support Request Template:</b>{" "}
        <a href="/support/static_support_request.txt" download>
          Download Template
        </a>
      </div>
    </section>
  );
}
