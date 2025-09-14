// [WINDSURF FIXED ✅]
import React, { useEffect, useState } from "react";
import axios from "axios";
import PropTypes from "prop-types"; // [WINDSURF FIXED]

const FILTERS = [
  { label: "All", fn: () => true },
  {
    label: "Suspicious",
    fn: (log) =>
      log.message &&
      /suspicious|manual review|rate limit|error/i.test(log.message),
  },
  {
    label: "Compliance",
    fn: (log) => log.message && /compliance|audit|ethics/i.test(log.message),
  },
  {
    label: "Privacy",
    fn: (log) => log.message && /privacy|consent|cache/i.test(log.message),
  },
];

const AuditLogSearchPanel = () => {
  const [logs, setLogs] = useState([]);
  const [filter, setFilter] = useState(FILTERS[0]);
  const [search, setSearch] = useState(""); // Remove if not used in render or logic
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        const token: "YOUR_TOKEN_HERE"("token");
        const res = await axios.get("/api/monitor/activity", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setLogs(res.data);
      } catch (err) {
        console.error("Failed to fetch logs:", err);
      } // [WINDSURF FIXED] Minimal error handler
      setLoading(false);
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 30000);
    return () => clearInterval(interval);
  }, []);

  const filteredLogs = logs.filter(
    (log) =>
      filter.fn(log) &&
      (!search ||
        JSON.stringify(log).toLowerCase().includes(search.toLowerCase())),
  );

  return (
    <div
      className="theme-card"
      style={{
        background: "var(--background)",
        color: "var(--text)",
        boxShadow: "var(--shadow-md)",
        borderRadius: "var(--border-radius-lg)",
        padding: "2rem",
        marginBottom: "2rem",
      }}
    >
      <h3 style={{ color: "var(--accent)" }}>Audit Log Search</h3>
      <div style={{ display: "flex", gap: "1rem", margin: "1rem 0" }}>
        <input
          type="text"
          placeholder="Search logs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            borderRadius: 6,
            border: "1px solid var(--border)",
            padding: "0.5rem 1rem",
            background: "var(--secondary)",
            color: "var(--text)",
          }}
          aria-label="Search logs"
        />
        <select
          value={filter.label}
          onChange={(e) =>
            setFilter(FILTERS.find((f) => f.label === e.target.value))
          }
          style={{
            borderRadius: 6,
            border: "1px solid var(--border)",
            padding: "0.5rem",
            background: "var(--secondary)",
            color: "var(--text)",
          }}
          aria-label="Filter logs"
        >
          {FILTERS.map((f) => (
            <option key={f.label} value={f.label}>
              {f.label}
            </option>
          ))}
        </select>
      </div>
      <div style={{ maxHeight: 260, overflowY: "auto", marginTop: "1rem" }}>
        {loading ? (
          <div>Loading logs...</div>
        ) : filteredLogs.length === 0 ? (
          <div>No logs found.</div>
        ) : (
          filteredLogs.map((log, i) => (
            <div
              key={i}
              style={{
                background: "var(--secondary)",
                borderRadius: "8px",
                padding: "0.75rem 1rem",
                marginBottom: "0.5rem",
                boxShadow: "var(--shadow-xs)",
                color: /error|suspicious|manual review|rate limit/i.test(
                  JSON.stringify(log),
                )
                  ? "var(--warning)"
                  : "var(--text)",
              }}
            >
              <div style={{ fontWeight: 600 }}>
                {log.message || log.action || log.event || "Log Entry"}
              </div>
              <div style={{ fontSize: "0.85rem", color: "var(--cta)" }}>
                {log.timestamp || log.timestamp_sim}
              </div>
              {log.status && (
                <span style={{ fontSize: "0.8rem", fontWeight: 500 }}>
                  {log.status}
                </span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// No props for AuditLogSearchPanel; PropTypes not required. [WINDSURF FIXED]

export default AuditLogSearchPanel; // [WINDSURF FIXED]
