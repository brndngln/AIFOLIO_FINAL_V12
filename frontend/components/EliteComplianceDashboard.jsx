import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Grid, Paper, Button, Chip, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress, Select, MenuItem, InputLabel, FormControl, Snackbar } from '@mui/material';

const statusColors = {
  ok: 'success',
  warning: 'warning',
  danger: 'error',
  escalated: 'secondary',
};

function maskReviewer(id) {
  if (!id) return '';
  return id.slice(0,2) + '***' + id.slice(-2);
}

const EliteComplianceDashboard = () => {
  const [violations, setViolations] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [vaultFilter, setVaultFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState('');

  useEffect(() => {
    fetchAll();
  }, []);

  const fetchAll = () => {
    setLoading(true);
    Promise.all([
      axios.get('/api/compliance/violations'),
      axios.get('/api/reviewer/leaderboard')
    ]).then(([v, l]) => {
      setViolations(v.data);
      setLeaderboard(l.data);
    }).finally(() => setLoading(false));
  };

  const handleExport = (type, docId) => {
    setSnackbar('Exporting...');
    axios.get(`/api/report/export_${type}${docId ? `?doc_id=${docId}` : ''}`)
      .then(res => {
        setSnackbar(`Exported: ${res.data.file || 'Ready for download'}`);
      })
      .catch(() => setSnackbar('Export failed.'));
  };

  const handleRemediate = (idx) => {
    axios.post('/api/remediation/apply', { idx, admin_id: 'admin' })
      .then(() => { setSnackbar('Remediation applied!'); fetchAll(); })
      .catch(() => setSnackbar('Remediation failed.'));
  };

  const handleRollback = (idx) => {
    axios.post('/api/remediation/rollback', { idx })
      .then(() => { setSnackbar('Remediation rolled back!'); fetchAll(); })
      .catch(() => setSnackbar('Rollback failed.'));
  };

  const filtered = violations.filter(v =>
    (statusFilter === 'all' || v.status === statusFilter) &&
    (severityFilter === 'all' || v.severity === severityFilter) &&
    (vaultFilter === 'all' || v.doc_id === vaultFilter)
  );

  const vaults = Array.from(new Set(violations.map(v => v.doc_id)));

  return (
    <Box sx={{ p: 3, bgcolor: '#eaeaea', borderRadius: 2, mb: 2 }}>
      <Typography variant="h4" mb={3}>AIFOLIO™ Elite Compliance Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" mb={2}>Compliance Feed</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth><InputLabel>Status</InputLabel><Select value={statusFilter} label="Status" onChange={e=>setStatusFilter(e.target.value)}><MenuItem value="all">All</MenuItem><MenuItem value="open">Open</MenuItem><MenuItem value="resolved">Resolved</MenuItem><MenuItem value="escalated">Escalated</MenuItem></Select></FormControl>
              </Grid>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth><InputLabel>Severity</InputLabel><Select value={severityFilter} label="Severity" onChange={e=>setSeverityFilter(e.target.value)}><MenuItem value="all">All</MenuItem><MenuItem value="critical">Critical</MenuItem><MenuItem value="major">Major</MenuItem><MenuItem value="minor">Minor</MenuItem><MenuItem value="info">Info</MenuItem></Select></FormControl>
              </Grid>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth><InputLabel>Vault</InputLabel><Select value={vaultFilter} label="Vault" onChange={e=>setVaultFilter(e.target.value)}><MenuItem value="all">All</MenuItem>{vaults.map(v => <MenuItem key={v} value={v}>{v}</MenuItem>)}</Select></FormControl>
              </Grid>
              <Grid item xs={12} md={3}>
                <Button fullWidth variant="contained" color="primary" onClick={()=>handleExport('csv')}>Export All CSV</Button>
              </Grid>
            </Grid>
            {loading ? <CircularProgress sx={{ mt: 4 }} /> : (
              <Table size="small" sx={{ mt: 2 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Vault</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Severity</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>SLA</TableCell>
                    <TableCell>Reviewer</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filtered.map((v, i) => (
                    <TableRow key={i}>
                      <TableCell>{v.doc_id}</TableCell>
                      <TableCell>{v.description}</TableCell>
                      <TableCell><Chip label={v.severity} color={v.severity==='critical'?'error':v.severity==='major'?'warning':'info'} /></TableCell>
                      <TableCell><Chip label={v.status} color={statusColors[v.sla_status]||'default'} /></TableCell>
                      <TableCell><Chip label={v.sla_status} color={statusColors[v.sla_status]||'default'} /></TableCell>
                      <TableCell>{maskReviewer(v.assigned_reviewer)}</TableCell>
                      <TableCell>
                        {v.status==='open' && <Button size="small" color="success" onClick={()=>handleRemediate(i)}>Remediate</Button>}
                        {v.status==='resolved' && <Button size="small" color="warning" onClick={()=>handleRollback(i)}>Rollback</Button>}
                        <Button size="small" color="info" onClick={()=>handleExport('pdf', v.doc_id)}>Export PDF</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" mb={2}>Reviewer Leaderboard</Typography>
            {loading ? <CircularProgress /> : (
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Accuracy</TableCell>
                    <TableCell>Resolved</TableCell>
                    <TableCell>Badges</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {leaderboard.map((r, i) => (
                    <TableRow key={i}>
                      <TableCell>{r.name}</TableCell>
                      <TableCell>{(r.accuracy*100).toFixed(1)}%</TableCell>
                      <TableCell>{r.resolved}</TableCell>
                      <TableCell>{r.badges.map((b,j)=><Chip key={j} label={b} color="primary" sx={{mr:0.5}} />)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </Paper>
        </Grid>
      </Grid>
      <Snackbar open={!!snackbar} autoHideDuration={4000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Box>
  );
};
export default EliteComplianceDashboard;
