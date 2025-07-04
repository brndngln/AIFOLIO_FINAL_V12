import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Grid, Paper, CircularProgress, Chip, Stack } from '@mui/material';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

const AdvancedAnalyticsDashboard = () => {
  const [usage, setUsage] = useState({});
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState({ total: 0, keys: 0, spikes: 0 });

  useEffect(() => {
    Promise.all([
      axios.get('/api/usage/metrics'),
      axios.get('/api/usage/anomalies')
    ]).then(([usageRes, anomalyRes]) => {
      setUsage(usageRes.data);
      setAnomalies(anomalyRes.data);
      let total = 0, keys = 0;
      Object.values(usageRes.data).forEach(dayObj => {
        total += Object.values(dayObj).reduce((a, b) => a + b, 0);
        keys++;
      });
      setSummary({ total, keys, spikes: anomalyRes.data.length });
    }).finally(() => setLoading(false));
  }, []);

  const keys = Object.keys(usage);
  const labels = keys.length ? Object.keys(usage[keys[0]]) : [];
  const lineData = {
    labels,
    datasets: keys.map((k, i) => ({
      label: k,
      data: Object.values(usage[k]),
      borderColor: `hsl(${i*60},70%,50%)`,
      backgroundColor: `hsla(${i*60},70%,50%,0.2)`,
      fill: false,
      tension: 0.2,
      pointRadius: 2
    }))
  };
  const barData = {
    labels: keys,
    datasets: [{
      label: 'Total Usage',
      data: keys.map(k => Object.values(usage[k]).reduce((a,b)=>a+b,0)),
      backgroundColor: keys.map((_,i)=>`hsla(${i*60},70%,50%,0.4)`)
    }]
  };
  const doughnutData = {
    labels: keys,
    datasets: [{
      data: keys.map(k => Object.values(usage[k]).reduce((a,b)=>a+b,0)),
      backgroundColor: keys.map((_,i)=>`hsla(${i*60},70%,50%,0.6)`)
    }]
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h5" mb={2}>Advanced Analytics Dashboard</Typography>
      {loading ? <CircularProgress /> : (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Secret Usage Over Time</Typography>
              <Line data={lineData} options={{ plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } }} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Usage by Key</Typography>
              <Bar data={barData} options={{ plugins: { legend: { display: false } }, indexAxis: 'y', scales: { x: { beginAtZero: true } } }} />
            </Paper>
          </Grid>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1">Usage Distribution</Typography>
              <Doughnut data={doughnutData} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
              <Chip label={`Total Calls: ${summary.total}`} color="primary" />
              <Chip label={`Tracked Keys: ${summary.keys}`} color="success" />
              <Chip label={`Spikes: ${summary.spikes}`} color="error" />
            </Stack>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};
export default AdvancedAnalyticsDashboard;
