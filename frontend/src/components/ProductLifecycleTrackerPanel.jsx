import React from "react";
import HyperEliteVaultBadge from "../../components/HyperEliteVaultBadge";

export default function ProductLifecycleTrackerPanel() {
  const features = [
    {
      label: "Static tracker",
      desc: "Tracker for vault product lifecycle stages (draft, review, live, archive)",
    },
    { label: "OWNER can update", desc: "OWNER can update stage manually" },
    {
      label: "Audit-logged changes",
      desc: "All changes are statically audit-logged",
    },
  ];
  return (
    <section
      aria-labelledby="product-lifecycle-heading"
      style={{
        background: "#f8fafc",
        borderRadius: 12,
        padding: 24,
        marginBottom: 24,
        boxShadow: "0 1px 4px #e0e7ef",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginBottom: 10,
        }}
      >
        <h3
          id="product-lifecycle-heading"
          style={{
            color: "#0ea5e9",
            fontWeight: 700,
            margin: 0,
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          Product Lifecycle Tracker
          <HyperEliteVaultBadge tooltip={true} external={false} />
        </h3>
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
          aria-label="Help: What is the Lifecycle Tracker?"
          title="Static, deterministic tracker for vault lifecycle. OWNER controls all stages."
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
        aria-label="Product lifecycle features"
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
    </section>
  );
}
