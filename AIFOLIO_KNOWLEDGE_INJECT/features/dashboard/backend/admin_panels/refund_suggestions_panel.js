// Refund Suggestions Panel Stub
// Displays refund suggestions from refund_optimizer.py
// Fetches from backend API endpoint

import React, { useEffect, useState } from "react";

export default function RefundSuggestionsPanel() {
  const [suggestions, setSuggestions] = useState([]);
  useEffect(() => {
    fetch("/api/refund_suggestions")
      .then((res) => res.json())
      .then(setSuggestions);
  }, []);
  return (
    <div>
      <h2>Refund Suggestions</h2>
      <ul>
        {suggestions.map((s, i) => (
          <li key={i}>
            {s.id}: {s.action}
          </li>
        ))}
      </ul>
    </div>
  );
}
