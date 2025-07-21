import React, { useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  TextField,
  MenuItem,
  Button,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  CircularProgress,
} from "@mui/material";

const LOGS = [
  { value: "rotation", label: "Secret Rotations" },
  { value: "anomaly", label: "Usage Spikes" },
  { value: "override", label: "Overrides" },
];

const AuditLogSearch = () => {
  const [log, setLog] = useState("rotation");
  const [q, setQ] = useState("");
  const [key, setKey] = useState("");
  const [status, setStatus] = useState("");
  const [admin, setAdmin] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true);
    axios
      .get("/api/audit/search", {
        params: { log, q, key, status, admin, start, end },
      })
      .then((res) => setResults(res.data))
      .finally(() => setLoading(false));
  };

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Audit Log Search
      </Typography>
      <Box sx={{ display: "flex", gap: 2, mb: 2, flexWrap: "wrap" }}>
        <TextField
          select
          label="Log Type"
          value={log}
          onChange={(e) => setLog(e.target.value)}
          size="small"
        >
          {LOGS.map((l) => (
            <MenuItem key={l.value} value={l.value}>
              {l.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="Free Text"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          size="small"
        />
        <TextField
          label="Key"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          size="small"
        />
        <TextField
          label="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          size="small"
        />
        <TextField
          label="Admin"
          value={admin}
          onChange={(e) => setAdmin(e.target.value)}
          size="small"
        />
        <TextField
          label="Start Date"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={start}
          onChange={(e) => setStart(e.target.value)}
          size="small"
        />
        <TextField
          label="End Date"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          size="small"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSearch}
          disabled={loading}
        >
          Search
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper sx={{ mt: 2 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                {results.length > 0 &&
                  Object.keys(results[0]).map((col) => (
                    <TableCell key={col}>{col}</TableCell>
                  ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {results.map((row, i) => (
                <TableRow key={i}>
                  {Object.values(row).map((val, j) => (
                    <TableCell key={j}>{String(val)}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
};
export default AuditLogSearch;
