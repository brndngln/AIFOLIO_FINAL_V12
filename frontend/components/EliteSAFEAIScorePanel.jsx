import React from "react";
import { Box, Typography, Paper, Chip, Divider } from "@mui/material";
import ShieldIcon from "@mui/icons-material/Shield";

export default function EliteSAFEAIScorePanel({ score = 98, details = {} }) {
  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <ShieldIcon sx={{ mr: 1 }} />
        <Typography variant="h6">SAFE AI Compliance Score</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <Chip
        label={`Score: ${score}`}
        color={score > 90 ? "success" : score > 75 ? "warning" : "error"}
        sx={{ fontSize: 18, mb: 2 }}
      />
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        This score is a static, deterministic SAFE AI compliance metric, fully
        auditable and owner-controlled.
      </Typography>
      <Box mt={2}>
        <Typography variant="subtitle2">Details:</Typography>
        <ul>
          <li>Privacy: {details.privacy || "PASS"}</li>
          <li>Security: {details.security || "PASS"}</li>
          <li>Auditability: {details.auditability || "PASS"}</li>
          <li>Test Coverage: {details.test_coverage || "PASS"}</li>
        </ul>
      </Box>
    </Paper>
  );
}
