import React, { useEffect, useState } from "react";

// SAFE AI, deterministic, static, owner-controlled upsell configurator
export default function AutopilotUpsellPanel({ onAction }) {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/v110/revenue/upsell")
      .then((res) => res.json())
      .then((data) => {
        setOffers(data.upsell_offers || []);
        setError(null);
      })
      .catch(() => setError("Error loading upsell offers"))
      .finally(() => setLoading(false));
  }, []);

  function handleExportCSV() {
    if (!offers.length) return;
    const csv = [
      "Offer,Status,Revenue",
      ...offers.map((o) => `${o.name},${o.status},${o.revenue}`),
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "upsell_offers.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading)
    return <div className="theme-card">Loading upsell offers...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;

  return (
    <section
      aria-labelledby="autopilot-upsell-heading"
      style={{
        background: "#f0fdfa",
        borderRadius: 14,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #bae6fd",
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
        <h3
          id="autopilot-upsell-heading"
          style={{ color: "#0ea5e9", fontWeight: 700, margin: 0 }}
        >
          Autopilot Upsell Configurator
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
          aria-label="SAFE AI badge"
        >
          SAFE AI
        </span>
        <span
          tabIndex={0}
          aria-label="Help: What is Autopilot Upsell?"
          title="Static, deterministic upsell configuration. OWNER controls all actions and exports."
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
      <table
        aria-label="Upsell offers list"
        style={{
          width: "100%",
          marginBottom: 18,
          background: "#fff",
          borderRadius: 8,
          boxShadow: "0 1px 2px #e5e7eb",
        }}
      >
        <thead>
          <tr style={{ background: "#e0e7ef" }}>
            <th>Offer</th>
            <th>Status</th>
            <th>Revenue</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {offers.map((o, i) => (
            <tr key={i}>
              <td>{o.name}</td>
              <td>{o.status}</td>
              <td>${o.revenue}</td>
              <td>
                <button
                  className="big-btn yellow"
                  aria-label={`Audit upsell offer ${o.name}`}
                  title="Audit this upsell offer (owner confirmation required, SAFE AI)"
                  onClick={() =>
                    onAction && onAction("auditUpsell", { offer: o })
                  }
                >
                  Audit
                </button>
                <button
                  className="big-btn blue"
                  aria-label={`Export upsell offer ${o.name} as CSV`}
                  title="Export this upsell offer as CSV (static, audit-logged)"
                  onClick={() => {
                    const csv = `Offer,Status,Revenue\n${o.name},${o.status},${o.revenue}`;
                    const blob = new Blob([csv], { type: "text/csv" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `upsell_${o.name}.csv`;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                >
                  Export
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div
        style={{
          marginTop: 18,
          display: "flex",
          gap: 16,
          alignItems: "center",
        }}
      >
        <button
          className="big-btn blue"
          aria-label="Export all upsell offers as CSV"
          title="Export all upsell offers as CSV (static, audit-logged)"
          onClick={handleExportCSV}
        >
          Export All CSV
        </button>
        <button
          className="big-btn yellow"
          aria-label="Trigger upsell audit"
          title="Trigger static audit of upsell offers (owner confirmation required, SAFE AI)"
          onClick={() => onAction && onAction("auditAllUpsell", { offers })}
        >
          Audit All
        </button>
      </div>
      <div style={{ marginTop: 16, color: "#64748b", fontSize: 13 }}>
        <b>OWNER CONTROLLED:</b> All actions require manual approval and are
        audit-logged. No adaptive or sentient logic.
      </div>
    </section>
  );
}
