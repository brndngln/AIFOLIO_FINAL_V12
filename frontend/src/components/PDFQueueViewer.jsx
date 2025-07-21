import React, { useEffect, useState } from "react";
import axios from "axios";

// [WINDSURF FIXED ✅]
export default function PDFQueueViewer({ token }) {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios
      .get("/api/pdf-queue", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setQueue(res.data))
      .catch(() => setQueue([]))
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="pdf-queue-viewer">
      <h3>PDF Generation Queue</h3>
      {loading ? (
        <div>Loading queue...</div>
      ) : (
        <ul>
          {queue.map((item, i) => (
            <li key={i}>
              {item.filename} — {item.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
