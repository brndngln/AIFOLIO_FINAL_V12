import React from "react";

export default function Stats({ events }) {
  const total = events.length;
  const errors = events.filter(
    (ev) => ev.errors && ev.errors.length > 0,
  ).length;
  const success = total - errors;
  const errorRate = total ? ((errors / total) * 100).toFixed(1) : 0;
  return (
    <div style={{ display: "flex", gap: 16, marginBottom: 20 }}>
      <div>
        <b>Total Events:</b> {total}
      </div>
      <div>
        <b>Success:</b> {success}
      </div>
      <div>
        <b>Errors:</b> {errors}
      </div>
      <div>
        <b>Error Rate:</b> {errorRate}%
      </div>
    </div>
  );
}
