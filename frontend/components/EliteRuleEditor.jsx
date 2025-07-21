import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Divider,
  Snackbar,
} from "@mui/material";
import EditNoteIcon from "@mui/icons-material/EditNote";

export default function EliteRuleEditor({ rules, onSave }) {
  const [currentRules, setCurrentRules] = useState(rules || "");
  const [snackbar, setSnackbar] = useState(false);

  const handleSave = () => {
    if (onSave) onSave(currentRules);
    setSnackbar(true);
  };

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <EditNoteIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Live Rule Editor</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <TextField
        label="Business & Compliance Rules (JSON)"
        multiline
        minRows={8}
        fullWidth
        value={currentRules}
        onChange={(e) => setCurrentRules(e.target.value)}
        variant="outlined"
      />
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={handleSave}
      >
        Save Rules
      </Button>
      <Snackbar
        open={snackbar}
        autoHideDuration={3000}
        onClose={() => setSnackbar(false)}
        message="Rules saved!"
      />
    </Paper>
  );
}
