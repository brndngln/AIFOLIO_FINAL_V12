import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  Divider,
  Select,
  MenuItem,
} from "@mui/material";
import BugReportIcon from "@mui/icons-material/BugReport";

const reviewers = ["Alpha", "Beta", "Gamma"];
const vaults = ["Vault 1", "Vault 2", "Vault 3"];

export default function EliteAuditSimulationPanel({ onSimulate }) {
  const [reviewer, setReviewer] = useState(reviewers[0]);
  const [vault, setVault] = useState(vaults[0]);

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <BugReportIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Audit Simulation Mode</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <Box mb={2}>
        <Typography variant="subtitle2">Simulate as Reviewer:</Typography>
        <Select
          value={reviewer}
          onChange={(e) => setReviewer(e.target.value)}
          sx={{ mr: 2 }}
        >
          {reviewers.map((r) => (
            <MenuItem key={r} value={r}>
              {r}
            </MenuItem>
          ))}
        </Select>
        <Typography variant="subtitle2" sx={{ ml: 4 }}>
          For Vault:
        </Typography>
        <Select value={vault} onChange={(e) => setVault(e.target.value)}>
          {vaults.map((v) => (
            <MenuItem key={v} value={v}>
              {v}
            </MenuItem>
          ))}
        </Select>
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={() => onSimulate && onSimulate(reviewer, vault)}
      >
        Run Audit Simulation
      </Button>
    </Paper>
  );
}
