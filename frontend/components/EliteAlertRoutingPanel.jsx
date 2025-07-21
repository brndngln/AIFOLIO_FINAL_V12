import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  Chip,
  Divider,
  Switch,
  FormControlLabel,
} from "@mui/material";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";

const DEFAULT_ROUTES = [
  { channel: "Slack", enabled: true },
  { channel: "Email", enabled: true },
  { channel: "SMS", enabled: false },
  { channel: "Discord", enabled: false },
  { channel: "Webhook", enabled: true },
];

export default function EliteAlertRoutingPanel({ routes, onChange }) {
  const [alertRoutes, setAlertRoutes] = useState(routes || DEFAULT_ROUTES);

  const handleToggle = (idx) => {
    const updated = alertRoutes.map((r, i) =>
      i === idx ? { ...r, enabled: !r.enabled } : r,
    );
    setAlertRoutes(updated);
    if (onChange) onChange(updated);
  };

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <NotificationsActiveIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Custom Alert Routing</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      {alertRoutes.map((route, idx) => (
        <FormControlLabel
          key={route.channel}
          control={
            <Switch
              checked={route.enabled}
              onChange={() => handleToggle(idx)}
            />
          }
          label={
            <Chip
              label={route.channel}
              color={route.enabled ? "primary" : "default"}
            />
          }
          sx={{ mr: 2, mb: 1 }}
        />
      ))}
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={() => onChange && onChange(alertRoutes)}
      >
        Save Routing
      </Button>
    </Paper>
  );
}
