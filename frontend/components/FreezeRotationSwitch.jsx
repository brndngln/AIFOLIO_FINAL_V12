import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Switch,
  Typography,
  Box,
  Alert,
  Button,
  Snackbar,
} from "@mui/material";
import MFAOverrideModal from "./MFAOverrideModal";

const FreezeRotationSwitch = ({ adminId }) => {
  const [enabled, setEnabled] = useState(true);
  const [loading, setLoading] = useState(false);
  const [lastChanged, setLastChanged] = useState("");
  const [error, setError] = useState("");
  const [mfaOpen, setMfaOpen] = useState(false);
  const [mfaError, setMfaError] = useState("");
  const [mfaLoading, setMfaLoading] = useState(false);
  const [snackbar, setSnackbar] = useState("");

  const refreshStatus = () => {
    axios.get("/api/rotation/enabled").then((res) => {
      setEnabled(res.data.enabled);
      setLastChanged(res.data.timestamp);
    });
  };

  useEffect(() => {
    refreshStatus();
  }, []);

  const handleToggle = () => {
    setMfaOpen(true);
    setMfaError("");
  };

  const handleMfaSubmit = (code) => {
    setMfaLoading(true);
    axios
      .post("/api/rotation/toggle", { adminId, code, enabled: !enabled })
      .then((res) => {
        setEnabled(res.data.enabled);
        setLastChanged(res.data.timestamp);
        setMfaOpen(false);
        setMfaError("");
        setSnackbar(
          res.data.enabled ? "Rotations resumed." : "Rotations paused.",
        );
      })
      .catch((err) => {
        setMfaError("MFA failed or unauthorized.");
      })
      .finally(() => setMfaLoading(false));
  };

  return (
    <Box sx={{ p: 2, bgcolor: "#fff", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6">Rotation Control</Typography>
      <Box sx={{ display: "flex", alignItems: "center", mt: 1 }}>
        <Typography
          color={enabled ? "success.main" : "error.main"}
          sx={{ fontWeight: "bold", mr: 2 }}
        >
          {enabled ? "🟢 Rotations Active" : "🔴 Rotations Paused"}
        </Typography>
        <Switch
          checked={enabled}
          onChange={handleToggle}
          color="primary"
          disabled={loading}
        />
      </Box>
      <Typography variant="caption" color="text.secondary">
        Last changed: {lastChanged || "N/A"}
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mt: 1 }}>
          {error}
        </Alert>
      )}
      <MFAOverrideModal
        open={mfaOpen}
        onClose={() => setMfaOpen(false)}
        onSubmit={handleMfaSubmit}
        error={mfaError}
        loading={mfaLoading}
      />
      <Snackbar
        open={!!snackbar}
        autoHideDuration={3000}
        onClose={() => setSnackbar("")}
        message={snackbar}
      />
    </Box>
  );
};
export default FreezeRotationSwitch;
