import React from "react";

export default function BatchPanel({ title, items }) {
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
      <h3 style={{ color: "#2563eb", fontWeight: 700, marginBottom: 12 }}>
        {title}
      </h3>
      <ul style={{ listStyle: "none", padding: 0, fontSize: 15 }}>
        {items.map((item, i) => (
          <li key={i} style={{ marginBottom: 8 }}>
            <span style={{ color: "#059669", fontWeight: 600 }}>✔</span> {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
