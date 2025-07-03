import React, { useEffect, useState } from 'react';
import { Paper, Typography, Divider, Grid, CircularProgress, Button } from '@mui/material';

export default function EliteSecurityPerformancePanel() {
  const [audit, setAudit] = useState(null);
  const [latency, setLatency] = useState(null);
  const [load, setLoad] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [a, l, ld] = await Promise.all([
        fetch('/api/security/audit').then(r=>r.json()),
        fetch('/api/performance/latency').then(r=>r.json()),
        fetch('/api/performance/load').then(r=>r.json()),
      ]);
      setAudit(a);
      setLatency(l);
      setLoad(ld);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { fetchAll(); }, []);

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" mb={2}>Elite Security & Performance Audit</Typography>
      <Divider sx={{ mb: 2 }} />
      <Button variant="outlined" onClick={fetchAll} sx={{ mb: 2 }}>Refresh Audit</Button>
      {loading ? <CircularProgress /> : (
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1">Security Audit</Typography>
            <pre style={{background:'#f9f9f9',padding:8,borderRadius:4,fontSize:13}}>{JSON.stringify(audit, null, 2)}</pre>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1">API Latency</Typography>
            <pre style={{background:'#f9f9f9',padding:8,borderRadius:4,fontSize:13}}>{JSON.stringify(latency, null, 2)}</pre>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1">Load Simulation</Typography>
            <pre style={{background:'#f9f9f9',padding:8,borderRadius:4,fontSize:13}}>{JSON.stringify(load, null, 2)}</pre>
          </Grid>
        </Grid>
      )}
    </Paper>
  );
}
