import React from "react";
import { Box, Typography, Paper, Button, Divider } from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";

export default function EliteExportPanel({ onExport }) {
  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <DownloadIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Multi-Channel Export</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <Button
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        onClick={() => onExport("notion")}
      >
        Export to Notion
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        onClick={() => onExport("airtable")}
      >
        Export to Airtable
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        onClick={() => onExport("pdf")}
      >
        Export PDF
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        onClick={() => onExport("csv")}
      >
        Export CSV
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mr: 2 }}
        onClick={() => onExport("api")}
      >
        Export to Partner API
      </Button>
    </Paper>
  );
}
