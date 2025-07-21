import React, { useEffect, useState } from "react";

// SAFE AI, deterministic, static, owner-controlled referral management
export default function ReferralManagementPanel({ onAction }) {
  const [referrals, setReferrals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/v110/revenue/referrals")
      .then((res) => res.json())
      .then((data) => {
        setReferrals(data.referrals || []);
        setError(null);
      })
      .catch(() => setError("Error loading referrals"))
      .finally(() => setLoading(false));
  }, []);

  function handleExportCSV() {
    if (!referrals.length) return;
    const csv = [
      "Referrer,Referred,Status,Revenue",
      ...referrals.map(
        (r) => `${r.referrer},${r.referred},${r.status},${r.revenue}`,
      ),
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "referrals.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) return <div className="theme-card">Loading referrals...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;

  return (
    <section
      aria-labelledby="referral-management-heading"
      style={{
        background: "#f3f4f6",
        borderRadius: 14,
        padding: 32,
        marginBottom: 32,
        boxShadow: "0 2px 8px #cbd5e1",
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
          id="referral-management-heading"
          style={{ color: "#0ea5e9", fontWeight: 700, margin: 0 }}
        >
          Referral Management
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
          aria-label="Help: What is Referral Management?"
          title="Static, deterministic referral management. OWNER controls all actions and exports."
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
        aria-label="Referral list"
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
            <th>Referrer</th>
            <th>Referred</th>
            <th>Status</th>
            <th>Revenue</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {referrals.map((r, i) => (
            <tr key={i}>
              <td>{r.referrer}</td>
              <td>{r.referred}</td>
              <td>{r.status}</td>
              <td>${r.revenue}</td>
              <td>
                <button
                  className="big-btn yellow"
                  aria-label={`Audit referral from ${r.referrer} to ${r.referred}`}
                  title="Audit this referral (owner confirmation required, SAFE AI)"
                  onClick={() =>
                    onAction && onAction("auditReferral", { referral: r })
                  }
                >
                  Audit
                </button>
                <button
                  className="big-btn blue"
                  aria-label={`Export referral from ${r.referrer} to ${r.referred} as CSV`}
                  title="Export this referral row as CSV (static, audit-logged)"
                  onClick={() => {
                    const csv = `Referrer,Referred,Status,Revenue\n${r.referrer},${r.referred},${r.status},${r.revenue}`;
                    const blob = new Blob([csv], { type: "text/csv" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `referral_${r.referrer}_${r.referred}.csv`;
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
          aria-label="Export all referrals as CSV"
          title="Export all referrals as CSV (static, audit-logged)"
          onClick={handleExportCSV}
        >
          Export All CSV
        </button>
        <button
          className="big-btn yellow"
          aria-label="Trigger referral audit"
          title="Trigger static audit of referrals (owner confirmation required, SAFE AI)"
          onClick={() =>
            onAction && onAction("auditAllReferrals", { referrals })
          }
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
