import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Button,
  TextField,
  MenuItem,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  CircularProgress,
  Snackbar,
} from "@mui/material";

const TYPES = [
  { value: "compliance_review", label: "Compliance Review" },
  { value: "incident_report", label: "Incident Report" },
  { value: "audit_request", label: "Audit Request" },
];

const RegulatoryWorkflowPanel = ({ adminId }) => {
  const [type, setType] = useState("compliance_review");
  const [payload, setPayload] = useState("");
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState("");

  const fetchLogs = () => {
    setLoading(true);
    axios
      .get("/api/regulatory/list")
      .then((res) => setLogs(res.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const handleSubmit = () => {
    axios
      .post("/api/regulatory/submit", { type, payload, admin_id: adminId })
      .then(() => {
        setSnackbar("Submitted!");
        fetchLogs();
        setPayload("");
      })
      .catch(() => setSnackbar("Submission failed."));
  };

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Regulatory Workflow Submission
      </Typography>
      <Box sx={{ display: "flex", gap: 2, mb: 2, flexWrap: "wrap" }}>
        <TextField
          select
          label="Type"
          value={type}
          onChange={(e) => setType(e.target.value)}
          size="small"
        >
          {TYPES.map((t) => (
            <MenuItem key={t.value} value={t.value}>
              {t.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="Payload"
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
          size="small"
          multiline
          minRows={1}
          sx={{ flex: 1 }}
        />
        <Button variant="contained" onClick={handleSubmit} disabled={!payload}>
          Submit
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper sx={{ mt: 2 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Submitted At</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Admin</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Payload</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {logs.map((row, i) => (
                <TableRow key={i}>
                  <TableCell>{row.submitted_at}</TableCell>
                  <TableCell>{row.type}</TableCell>
                  <TableCell>{row.admin_id}</TableCell>
                  <TableCell>{row.status}</TableCell>
                  <TableCell>{row.payload}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      <Snackbar
        open={!!snackbar}
        autoHideDuration={3000}
        onClose={() => setSnackbar("")}
        message={snackbar}
      />
    </Box>
  );
};
export default RegulatoryWorkflowPanel;
