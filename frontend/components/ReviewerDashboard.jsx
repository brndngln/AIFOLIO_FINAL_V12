import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Table, TableHead, TableRow, TableCell, TableBody, Paper, CircularProgress, Chip, Button } from '@mui/material';

const ReviewerDashboard = () => {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    axios.get('/api/regulatory/list').then(res => setWorkflows(res.data)).finally(() => setLoading(false));
  }, []);

  const handleReview = (i, status) => {
    // For demo: just update status locally
    setWorkflows(ws => ws.map((w, idx) => idx === i ? { ...w, status } : w));
    // In production, submit status update to backend/audit log
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Regulatory Reviewer Dashboard</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Submitted At</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Admin</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Payload</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {workflows.map((row, i) => (
                <TableRow key={i} selected={selected === i}>
                  <TableCell>{row.submitted_at}</TableCell>
                  <TableCell>{row.type}</TableCell>
                  <TableCell>{row.admin_id}</TableCell>
                  <TableCell><Chip label={row.status} color={row.status==='approved'?'success':row.status==='rejected'?'error':'warning'} /></TableCell>
                  <TableCell>{row.payload}</TableCell>
                  <TableCell>
                    <Button size="small" color="success" onClick={()=>handleReview(i,'approved')}>Approve</Button>
                    <Button size="small" color="error" onClick={()=>handleReview(i,'rejected')}>Reject</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      {selected !== null && (
        <Box sx={{ mt: 2, p: 2, bgcolor: '#fff', borderRadius: 2 }}>
          <Typography variant="subtitle1">Workflow Details</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{JSON.stringify(workflows[selected], null, 2)}</pre>
        </Box>
      )}
    </Box>
  );
};
export default ReviewerDashboard;
