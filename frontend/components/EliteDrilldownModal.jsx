import React from 'react';
import { Modal, Box, Typography, Divider, Button, Chip } from '@mui/material';
import HistoryIcon from '@mui/icons-material/History';
import AssignmentIcon from '@mui/icons-material/Assignment';

export default function EliteDrilldownModal({ open, onClose, event }) {
  if (!event) return null;
  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', bgcolor: '#fff', p: 4, borderRadius: 2, minWidth: 400, maxWidth: 600 }}>
        <Box display="flex" alignItems="center" mb={2}>
          <HistoryIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Event Drilldown</Typography>
        </Box>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="subtitle1" gutterBottom><AssignmentIcon sx={{ mr: 1 }} />Event Type: <b>{event.event_type}</b></Typography>
        <Typography variant="body2" gutterBottom>Status: <Chip label={event.status} color={event.status==='critical'?'error':'primary'} /></Typography>
        <Typography variant="body2" gutterBottom>Timestamp: {event.timestamp}</Typography>
        <Typography variant="body2" gutterBottom>Reviewer: {event.reviewer}</Typography>
        <Typography variant="body2" gutterBottom>Payload:</Typography>
        <Box sx={{ bgcolor: '#f3f3f3', borderRadius: 1, p: 2, mb: 2, fontFamily: 'monospace', fontSize: 13 }}>
          {JSON.stringify(event.payload, null, 2)}
        </Box>
        <Button variant="contained" color="primary" onClick={onClose}>Close</Button>
      </Box>
    </Modal>
  );
}
