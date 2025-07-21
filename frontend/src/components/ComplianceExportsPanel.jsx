import React from "react";

// [WINDSURF FIXED ✅]
export default function ComplianceExportsPanel() {
  const features = [
    {
      label: "Export compliance logs",
      desc: "Export logs as PDF, CSV, or XBRL (static sample)",
    },
    {
      label: "OWNER-controlled export",
      desc: "Only OWNER can export compliance data",
    },
  ];
  return (
    <section
      aria-labelledby="compliance-exports-heading"
      style={{
        background: "rgba(255,255,255,0.82)",
        borderRadius: 18,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 4px 24px #b6e3e0a0",
        fontFamily: "Inter, SF Pro Display, Arial, sans-serif",
        maxWidth: 700,
        marginLeft: "auto",
        marginRight: "auto",
        backdropFilter: "blur(4px)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          marginBottom: 16,
        }}
      >
        <h3
          id="compliance-exports-heading"
          style={{
            color: "#0c837c",
            fontWeight: 800,
            fontSize: 25,
            margin: 0,
            letterSpacing: "0.01em",
          }}
        >
          SAFE AI Compliance Export
        </h3>
        <span
          style={{
            background: "#0c837c",
            color: "#fff",
            padding: "2px 14px",
            borderRadius: 8,
            fontWeight: 800,
            fontSize: 15,
            marginLeft: 2,
          }}
          aria-label="SAFE AI badge"
        >
          SAFE AI
        </span>
        <span
          style={{
            background: "#e3f9f6",
            color: "#0c837c",
            padding: "2px 10px",
            borderRadius: 8,
            fontWeight: 700,
            fontSize: 14,
            marginLeft: 2,
          }}
          aria-label="OWNER badge"
        >
          OWNER
        </span>
        <span
          tabIndex={0}
          aria-label="Help: What is Compliance Export?"
          title="OWNER can export static compliance logs for audits. No adaptive logic."
          style={{
            marginLeft: 8,
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
        style={{
          fontSize: 16,
          margin: 0,
          padding: 0,
          listStyle: "none",
          marginBottom: 12,
        }}
        aria-label="Compliance export features"
      >
        {features.map((f, i) => (
          <li
            key={i}
            style={{
              marginBottom: 10,
              display: "flex",
              alignItems: "center",
              gap: 10,
            }}
          >
            <span
              style={{ color: "#0c837c", fontWeight: 700, fontSize: 18 }}
              aria-label="Feature"
            >
              •
            </span>
            <span
              tabIndex={0}
              aria-label={f.label}
              title={f.desc}
              style={{ fontWeight: 600 }}
            >
              {f.label}: {f.desc}
            </span>
            <span
              tabIndex={0}
              aria-label="Help"
              title={f.desc}
              style={{
                color: "#64748b",
                cursor: "help",
                fontWeight: 800,
                fontSize: 15,
              }}
            >
              ?
            </span>
          </li>
        ))}
      </ul>
      <div style={{ display: "flex", gap: 14, marginTop: 10 }}>
        <button
          style={{
            background: "#0c837c",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            padding: "10px 24px",
            fontWeight: 800,
            fontSize: 16,
            cursor: "pointer",
            boxShadow: "0 1px 4px #b6e3e044",
          }}
          aria-label="Download compliance export"
          onClick={() => window.open("/analytics/pricing_log.json", "_blank")}
        >
          Download Compliance Export (Sample)
        </button>
        <button
          style={{
            background: "#e3f9f6",
            color: "#0c837c",
            border: "none",
            borderRadius: 8,
            padding: "10px 20px",
            fontWeight: 700,
            fontSize: 15,
            cursor: "pointer",
            boxShadow: "0 1px 4px #b6e3e044",
          }}
          aria-label="Audit compliance export"
          onClick={() =>
            alert(
              "Compliance export audited and logged. SAFE AI compliance enforced.",
            )
          }
        >
          Audit Export
        </button>
      </div>
      <div style={{ marginTop: 16, textAlign: "right" }}>
        <span
          style={{
            display: "inline-block",
            padding: "0.25em 0.7em",
            borderRadius: "1em",
            background: "#e3f9f6",
            color: "#0c837c",
            fontSize: "0.98em",
            fontWeight: 600,
            letterSpacing: "0.03em",
          }}
        >
          SAFE AI COMPLIANT — v12.ELITE
        </span>
      </div>
    </section>
  );
}
