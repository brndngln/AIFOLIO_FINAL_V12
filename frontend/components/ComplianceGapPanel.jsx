import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
  Alert,
} from "@mui/material";

const ComplianceGapPanel = () => {
  const [gaps, setGaps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/api/compliance/gaps")
      .then((res) => setGaps(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Dynamic Compliance Gap Analysis
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : gaps.length === 0 ? (
        <Alert severity="success">No gaps found. All mapped!</Alert>
      ) : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Standard</TableCell>
                <TableCell>Control</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {gaps.map((g, i) => (
                <TableRow key={i}>
                  <TableCell>{g.standard}</TableCell>
                  <TableCell>{g.control}</TableCell>
                  <TableCell>{g.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
};
export default ComplianceGapPanel;
