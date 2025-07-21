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
  Chip,
} from "@mui/material";

const ReviewerAnalyticsPanel = () => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/api/reviewer/analytics")
      .then((res) => setStats(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Reviewer Performance Analytics
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Reviewer</TableCell>
                <TableCell>Approvals</TableCell>
                <TableCell>Rejections</TableCell>
                <TableCell>Workflows</TableCell>
                <TableCell>Last Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {stats.map((s, i) => (
                <TableRow key={i}>
                  <TableCell>{s.reviewer}</TableCell>
                  <TableCell>
                    <Chip label={s.approvals} color="success" />
                  </TableCell>
                  <TableCell>
                    <Chip label={s.rejections} color="error" />
                  </TableCell>
                  <TableCell>
                    <Chip label={s.workflows} color="info" />
                  </TableCell>
                  <TableCell>{s.last_action}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
};
export default ReviewerAnalyticsPanel;
