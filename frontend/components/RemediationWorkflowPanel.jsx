import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress, Button, Snackbar, Chip } from '@mui/material';

const RemediationWorkflowPanel = ({ adminId }) => {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState('');

  const fetchWorkflows = () => {
    setLoading(true);
    axios.get('/api/remediation/list').then(res => setWorkflows(res.data)).finally(() => setLoading(false));
  };

  useEffect(() => { fetchWorkflows(); }, []);

  const handleSubmit = (control) => {
    axios.post('/api/remediation/submit', { control, admin_id: adminId })
      .then(() => { setSnackbar('Remediation workflow submitted!'); fetchWorkflows(); })
      .catch(() => setSnackbar('Submission failed.'));
  };

  const handleUpdate = (idx, status) => {
    axios.post('/api/remediation/update_status', { idx, status, reviewer: adminId })
      .then(() => { setSnackbar('Status updated!'); fetchWorkflows(); })
      .catch(() => setSnackbar('Update failed.'));
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Remediation Workflow Automation</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Control</TableCell>
                <TableCell>Recommendation</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>History</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {workflows.map((w, i) => (
                <TableRow key={i}>
                  <TableCell>{w.control}</TableCell>
                  <TableCell>{w.recommendation}</TableCell>
                  <TableCell><Chip label={w.status} color={w.status==='completed'?'success':w.status==='rejected'?'error':'warning'} /></TableCell>
                  <TableCell>
                    {w.history.map((h, j) => <div key={j}>{h.status} ({h.timestamp}){h.reviewer?` by ${h.reviewer}`:''}</div>)}
                  </TableCell>
                  <TableCell>
                    {w.status==='submitted' && <>
                      <Button size="small" color="success" onClick={()=>handleUpdate(i,'completed')}>Mark Complete</Button>
                      <Button size="small" color="error" onClick={()=>handleUpdate(i,'rejected')}>Reject</Button>
                    </>}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      <Snackbar open={!!snackbar} autoHideDuration={3000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Box>
  );
};
export default RemediationWorkflowPanel;
