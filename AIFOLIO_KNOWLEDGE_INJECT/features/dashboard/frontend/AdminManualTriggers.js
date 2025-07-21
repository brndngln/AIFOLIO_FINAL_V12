// AIFOLIO SAFE AI Admin Manual Triggers Component
// Allows admin to manually re-run analytics, resend receipts, and rebuild reports (all actions logged)
import React, { useState } from "react";
import { fetchAdminManualTrigger } from "./api";

export default function AdminManualTriggers() {
  const [result, setResult] = useState({});
  return (
    <div>
      <h2>Admin Manual Triggers</h2>
      <button onClick={async () => setResult(await fetchAdminManualTrigger())}>
        Re-run Analytics / Resend Receipts / Rebuild Reports
      </button>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}
