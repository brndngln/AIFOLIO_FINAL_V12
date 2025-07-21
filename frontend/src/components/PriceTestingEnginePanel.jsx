import React from "react";

export default function PriceTestingEnginePanel() {
  const features = [
    {
      label: "Multi-Price Test UI",
      desc: "OWNER can run static price tests ($17/$27/$37, etc)",
    },
    {
      label: "Auto-track Conversion/Revenue",
      desc: "Static log UI for pricing analytics",
    },
    {
      label: "Auto-pick Winning Price",
      desc: "Static logic to highlight best performer",
    },
    { label: "Logs", desc: "All price test logs are static, OWNER-exportable" },
  ];
  return (
    <section
      aria-labelledby="price-testing-engine-heading"
      style={{
        background: "#f1f5f9",
        borderRadius: 12,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #dbeafe",
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
          id="price-testing-engine-heading"
          style={{ color: "#0ea5e9", fontWeight: 800, fontSize: 24, margin: 0 }}
        >
          Autonomous Price Testing Engine
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
          aria-label="Help: What is the Price Testing Engine?"
          title="This engine statically tests and logs pricing performance. No adaptive or sentient logic."
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
        style={{ fontSize: 15, margin: 0, padding: 0, listStyle: "none" }}
        aria-label="Price testing engine features"
      >
        {features.map((f, i) => (
          <li
            key={i}
            style={{
              marginBottom: 8,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span
              style={{ color: "#0ea5e9", fontWeight: 600 }}
              aria-label="Feature"
            >
              •
            </span>
            <span tabIndex={0} aria-label={f.label} title={f.desc}>
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
      <div
        style={{
          marginTop: 18,
          background: "#e0e7ef",
          padding: 12,
          borderRadius: 8,
        }}
      >
        <b>Log files:</b> <code>/analytics/pricing_log.json</code>,{" "}
        <code>/analytics/price_tests/price_test_log.json</code>
      </div>
    </section>
  );
}
