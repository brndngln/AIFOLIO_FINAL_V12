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
  Button,
  CircularProgress,
  Snackbar,
  TextField,
} from "@mui/material";

const PolicyApprovalPanel = ({ reviewer }) => {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState("");
  const [rejectReason, setRejectReason] = useState({});

  const fetchApprovals = () => {
    setLoading(true);
    axios
      .get("/api/policy/approvals")
      .then((res) => setApprovals(res.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  const handleApprove = (idx) => {
    axios
      .post("/api/policy/approve", { idx, reviewer })
      .then(() => {
        setSnackbar("Approved!");
        fetchApprovals();
      })
      .catch(() => setSnackbar("Approval failed."));
  };
  const handleReject = (idx) => {
    axios
      .post("/api/policy/reject", {
        idx,
        reviewer,
        reason: rejectReason[idx] || "",
      })
      .then(() => {
        setSnackbar("Rejected!");
        fetchApprovals();
      })
      .catch(() => setSnackbar("Rejection failed."));
  };

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Policy Recommendation Approvals
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Status</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Submitter</TableCell>
                <TableCell>Approvals</TableCell>
                <TableCell>Rejections</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {approvals.map((a, i) => (
                <TableRow key={i}>
                  <TableCell>{a.status}</TableCell>
                  <TableCell>{a.recommendation.type}</TableCell>
                  <TableCell>{a.recommendation.description}</TableCell>
                  <TableCell>{a.submitter}</TableCell>
                  <TableCell>{a.approvals.length}</TableCell>
                  <TableCell>{a.rejections.length}</TableCell>
                  <TableCell>
                    {a.status === "pending" && (
                      <>
                        <Button
                          size="small"
                          color="success"
                          onClick={() => handleApprove(i)}
                        >
                          Approve
                        </Button>
                        <TextField
                          size="small"
                          placeholder="Reason"
                          value={rejectReason[i] || ""}
                          onChange={(e) =>
                            setRejectReason((rr) => ({
                              ...rr,
                              [i]: e.target.value,
                            }))
                          }
                          sx={{ width: 100, mx: 1 }}
                        />
                        <Button
                          size="small"
                          color="error"
                          onClick={() => handleReject(i)}
                        >
                          Reject
                        </Button>
                      </>
                    )}
                  </TableCell>
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
export default PolicyApprovalPanel;
