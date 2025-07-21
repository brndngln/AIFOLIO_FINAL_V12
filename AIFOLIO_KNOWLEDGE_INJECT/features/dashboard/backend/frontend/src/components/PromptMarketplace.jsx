import React, { useState, useEffect } from "react";

// Placeholder for backend API
const fetchPrompts = async () => [
  {
    id: 1,
    title: "Elite Sales Page",
    author: "admin",
    status: "approved",
    downloads: 42,
  },
  {
    id: 2,
    title: "High-Ticket Funnel",
    author: "partner01",
    status: "pending",
    downloads: 12,
  },
];

export default function PromptMarketplace() {
  const [prompts, setPrompts] = useState([]);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchPrompts().then(setPrompts);
  }, []);

  return (
    <div
      className="prompt-marketplace"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
      }}
    >
      <h2>Prompt Marketplace</h2>
      <div style={{ marginBottom: 16 }}>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="approved">Approved</option>
          <option value="pending">Pending</option>
        </select>
        <button
          style={{
            marginLeft: 16,
            background: "#00e6ff",
            color: "#181e2b",
            border: "none",
            borderRadius: 8,
            padding: "8px 16px",
            fontWeight: "bold",
          }}
        >
          Submit Prompt
        </button>
      </div>
      <table style={{ width: "100%", background: "#232b3b", borderRadius: 8 }}>
        <thead>
          <tr style={{ color: "#00e6ff" }}>
            <th>Title</th>
            <th>Author</th>
            <th>Status</th>
            <th>Downloads</th>
          </tr>
        </thead>
        <tbody>
          {prompts
            .filter((p) => filter === "all" || p.status === filter)
            .map((p) => (
              <tr key={p.id}>
                <td>{p.title}</td>
                <td>{p.author}</td>
                <td>{p.status}</td>
                <td>{p.downloads}</td>
              </tr>
            ))}
        </tbody>
      </table>
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          Submit, review, and monetize elite prompt sets. All submissions are
          owner-moderated and SAFE AI-compliant.
        </em>
      </div>
    </div>
  );
}
