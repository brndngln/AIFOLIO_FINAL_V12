import React, { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  Divider,
  Button,
  CircularProgress,
  Snackbar,
} from "@mui/material";

export default function EliteHeartbeatPanel() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState("");

  const fetchHeartbeat = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/heartbeat");
      const data = await res.json();
      setStatus(data);
      setSnackbar("Heartbeat checked!");
    } catch {
      setSnackbar("Heartbeat check failed");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchHeartbeat();
  }, []);

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        System Heartbeat
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Button variant="outlined" onClick={fetchHeartbeat} sx={{ mb: 2 }}>
        Check Heartbeat
      </Button>
      {loading && <CircularProgress />}
      {status && (
        <pre style={{ background: "#f9f9f9", padding: 16, borderRadius: 8 }}>
          {JSON.stringify(status, null, 2)}
        </pre>
      )}
      <Snackbar
        open={!!snackbar}
        autoHideDuration={3000}
        onClose={() => setSnackbar("")}
        message={snackbar}
      />
    </Paper>
  );
}
