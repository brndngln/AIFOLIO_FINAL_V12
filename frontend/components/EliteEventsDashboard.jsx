import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Button,
  Paper,
  Tabs,
  Tab,
  Badge,
  Chip,
  Tooltip,
  IconButton,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import ReplayIcon from "@mui/icons-material/Replay";
import EditIcon from "@mui/icons-material/Edit";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import SmsIcon from "@mui/icons-material/Sms";
import IntegrationInstructionsIcon from "@mui/icons-material/IntegrationInstructions";

const API_URL = "/api/events"; // Backend endpoint for event log and control

const statusColors = {
  success: "success",
  error: "error",
  pending: "info",
  retried: "warning",
};

function EventRow({ event, onRetrigger, onEdit }) {
  return (
    <Paper
      elevation={1}
      sx={{ p: 2, mb: 1, display: "flex", alignItems: "center", gap: 2 }}
    >
      <Badge
        color={statusColors[event.status] || "default"}
        badgeContent={
          event.status === "error" ? (
            <ErrorIcon color="error" />
          ) : (
            <CheckCircleIcon color="success" />
          )
        }
        anchorOrigin={{ vertical: "top", horizontal: "left" }}
      >
        <EventAvailableIcon />
      </Badge>
      <Box sx={{ flex: 1 }}>
        <Typography variant="subtitle2">{event.event_type}</Typography>
        <Typography variant="caption" color="text.secondary">
          {event.timestamp}
        </Typography>
        <Box sx={{ mt: 1, display: "flex", gap: 1, flexWrap: "wrap" }}>
          {Object.entries(event.payload).map(([k, v]) => (
            <Chip key={k} label={`${k}: ${JSON.stringify(v)}`} size="small" />
          ))}
        </Box>
        {event.integrations && (
          <Box sx={{ mt: 1, display: "flex", gap: 1 }}>
            {event.integrations.map((i) => (
              <Tooltip title={i} key={i}>
                <IntegrationInstructionsIcon fontSize="small" color="primary" />
              </Tooltip>
            ))}
          </Box>
        )}
      </Box>
      <Tooltip title="Retrigger">
        <IconButton onClick={() => onRetrigger(event)}>
          <ReplayIcon />
        </IconButton>
      </Tooltip>
      <Tooltip title="Edit Payload">
        <IconButton onClick={() => onEdit(event)}>
          <EditIcon />
        </IconButton>
      </Tooltip>
      {event.status === "error" && (
        <Tooltip title="Retry via SMS">
          <IconButton color="secondary">
            <SmsIcon />
          </IconButton>
        </Tooltip>
      )}
    </Paper>
  );
}

export default function EliteEventsDashboard() {
  const [events, setEvents] = useState([]);
  const [tab, setTab] = useState(0);
  const [loading, setLoading] = useState(true);
  const [editEvent, setEditEvent] = useState(null);
  const [editPayload, setEditPayload] = useState("");

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/log`);
      const data = await res.json();
      setEvents(data);
    } catch (e) {
      setEvents([]);
    }
    setLoading(false);
  };

  const handleRetrigger = async (event) => {
    await fetch(`${API_URL}/retrigger`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event_type: event.event_type,
        payload: event.payload,
      }),
    });
    fetchEvents();
  };

  const handleEdit = (event) => {
    setEditEvent(event);
    setEditPayload(JSON.stringify(event.payload, null, 2));
  };

  const handleEditSave = async () => {
    await fetch(`${API_URL}/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event_type: editEvent.event_type,
        payload: JSON.parse(editPayload),
      }),
    });
    setEditEvent(null);
    fetchEvents();
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: "bold" }}>
        Elite Events Dashboard
      </Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="All Events" />
        <Tab label="Errors" />
        <Tab label="Success" />
        <Tab label="Pending" />
      </Tabs>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box>
          {events
            .filter(
              (e) =>
                tab === 0 ||
                (tab === 1 && e.status === "error") ||
                (tab === 2 && e.status === "success") ||
                (tab === 3 && e.status === "pending"),
            )
            .map((event) => (
              <EventRow
                key={event.id}
                event={event}
                onRetrigger={handleRetrigger}
                onEdit={handleEdit}
              />
            ))}
        </Box>
      )}
      <Dialog
        open={!!editEvent}
        onClose={() => setEditEvent(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Event Payload</DialogTitle>
        <DialogContent>
          <TextField
            multiline
            minRows={6}
            fullWidth
            value={editPayload}
            onChange={(e) => setEditPayload(e.target.value)}
            variant="outlined"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditEvent(null)}>Cancel</Button>
          <Button onClick={handleEditSave} variant="contained">
            Save & Retrigger
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
