import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Grid, Paper, CircularProgress, Chip, Stack, Alert } from '@mui/material';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

const LiveComplianceDashboard = () => {
  const [usage, setUsage] = useState({});
  const [anomalies, setAnomalies] = useState([]);
  const [rootCauses, setRootCauses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState({ total: 0, keys: 0, spikes: 0, overrides: 0 });
  const [lastExport, setLastExport] = useState('');

  useEffect(() => {
    Promise.all([
      axios.get('/api/usage/metrics'),
      axios.get('/api/usage/anomalies'),
      axios.get('/api/anomaly/root_cause'),
      axios.get('/api/logs/secret_rotation'),
      axios.get('/api/logs/override_attempts')
    ]).then(([usageRes, anomalyRes, rootCauseRes, rotationRes, overrideRes]) => {
      setUsage(usageRes.data);
      setAnomalies(anomalyRes.data);
      setRootCauses(rootCauseRes.data);
      let total = 0, keys = 0;
      Object.values(usageRes.data).forEach(dayObj => {
        total += Object.values(dayObj).reduce((a, b) => a + b, 0);
        keys++;
      });
      setSummary({
        total,
        keys,
        spikes: anomalyRes.data.length,
        overrides: overrideRes.data.length
      });
    }).finally(() => setLoading(false));
    // Optionally, poll for live updates
    const interval = setInterval(()=>{
      axios.get('/api/compliance/export').then(()=>setLastExport(new Date().toLocaleString()));
    }, 60000);
    return ()=>clearInterval(interval);
  }, []);

  const anomalyLabels = anomalies.map(a => a.timestamp);
  const anomalyData = anomalies.map(a => a.current);

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h5" mb={2}>Live Compliance Dashboard</Typography>
      {loading ? <CircularProgress /> : (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Secret Usage Over Time</Typography>
              <Line data={{
                labels: Object.keys(usage[Object.keys(usage)[0]] || {}),
                datasets: Object.keys(usage).map((k, i) => ({
                  label: k,
                  data: Object.values(usage[k]),
                  borderColor: `hsl(${i*60},70%,50%)`,
                  backgroundColor: `hsla(${i*60},70%,50%,0.2)`,
                  fill: false,
                  tension: 0.2,
                  pointRadius: 2
                }))
              }} options={{ plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } }} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Anomaly Spikes</Typography>
              <Bar data={{ labels: anomalyLabels, datasets: [{ label: 'Spike Volume', data: anomalyData, backgroundColor: 'rgba(255,99,132,0.6)' }] }} options={{ plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Root Cause Distribution</Typography>
              <Doughnut data={{
                labels: rootCauses.map(r=>r.root_cause),
                datasets: [{ data: rootCauses.map(()=>1), backgroundColor: rootCauses.map((_,i)=>`hsla(${i*60},70%,50%,0.6)`) }]
              }} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
              <Chip label={`Total Calls: ${summary.total}`} color="primary" />
              <Chip label={`Tracked Keys: ${summary.keys}`} color="success" />
              <Chip label={`Spikes: ${summary.spikes}`} color="error" />
              <Chip label={`Overrides: ${summary.overrides}`} color="warning" />
              <Chip label={`Last Export: ${lastExport || 'N/A'}`} color="info" />
            </Stack>
          </Grid>
          <Grid item xs={12}>
            <Alert severity="info">All compliance data is live and exportable for audit at any time.</Alert>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};
export default LiveComplianceDashboard;
