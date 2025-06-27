import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Grid, Divider, Chip, CircularProgress, Button } from '@mui/material';

const analyticsEndpoints = [
  { label: 'Refund Risk', path: '/api/analytics/refund_risk', sample: { vault_id: 'vault_001', sales: [{id:1}], refunds: [{vault_id:'vault_001'}] } },
  { label: 'Churn & Retention', path: '/api/analytics/churn_retention', sample: { vault_id: 'vault_001', user_events: [{user_id:'u1',vault_id:'vault_001',event:'churn'}] } },
  { label: 'Asset Health', path: '/api/analytics/asset_health', sample: { vault_id: 'vault_001', assets: [{status:'ok',weight:2}] } },
  { label: 'Tone/Voice', path: '/api/analytics/tone_voice', sample: { text: 'Brand match text', brand_profile: 'Brand' } },
  { label: 'Reviewer Heatmap', path: '/api/analytics/reviewer_heatmap', sample: { reviewer_events: [{reviewer:'r1',event:'streak'}] } },
  { label: 'Funnel Analytics', path: '/api/analytics/funnel', sample: { vault_id: 'vault_001', funnel_events: [{type:'launch'}] } },
  { label: 'High-Ticket Leaderboard', path: '/api/analytics/high_ticket_leaderboard', sample: { vaults: [{profit:100,engagement:10,trend:5}] } },
];

export default function EliteAdvancedAnalyticsPanel() {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);

  const runAnalytics = async (endpoint, sample) => {
    setLoading(true);
    try {
      const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sample) });
      const data = await res.json();
      setResults(r => ({ ...r, [endpoint]: data }));
    } catch {
      setResults(r => ({ ...r, [endpoint]: { error: true } }));
    }
    setLoading(false);
  };

  useEffect(() => {
    analyticsEndpoints.forEach(a => runAnalytics(a.path, a.sample));
  }, []);

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" mb={2}>Elite Advanced Analytics</Typography>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        {analyticsEndpoints.map(a => (
          <Grid item xs={12} md={6} key={a.label}>
            <Paper sx={{ p: 2, mb: 2 }}>
              <Typography variant="subtitle1">{a.label}</Typography>
              <Button variant="outlined" size="small" sx={{ mb: 1 }} onClick={() => runAnalytics(a.path, a.sample)}>Run</Button>
              {loading ? <CircularProgress size={20} /> : (
                <pre style={{ background: '#f9f9f9', padding: 8, borderRadius: 4, fontSize: 13 }}>{JSON.stringify(results[a.path], null, 2)}</pre>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
}
