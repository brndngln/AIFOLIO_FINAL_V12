import React, { useEffect, useState } from 'react';
import { Paper, Typography, Button, Divider, Grid, CircularProgress, Snackbar } from '@mui/material';

export default function EliteComplianceExportsPanel() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [snackbar, setSnackbar] = useState('');

  const exportCompliance = async (type) => {
    setLoading(true);
    setSnackbar('Exporting...');
    try {
      const res = await fetch(`/api/export/compliance?type=${type}`);
      const data = await res.json();
      setResult(data);
      setSnackbar('Export complete!');
    } catch {
      setSnackbar('Export failed');
    }
    setLoading(false);
  };

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" mb={2}>Compliance Exports</Typography>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        <Grid item>
          <Button variant="contained" color="primary" onClick={() => exportCompliance('notion')}>Export to Notion</Button>
        </Grid>
        <Grid item>
          <Button variant="contained" color="secondary" onClick={() => exportCompliance('sheets')}>Export to Google Sheets</Button>
        </Grid>
        <Grid item>
          <Button variant="contained" color="info" onClick={() => exportCompliance('airtable')}>Export to Airtable</Button>
        </Grid>
      </Grid>
      {loading && <CircularProgress sx={{ mt: 2 }} />}
      {result && <pre style={{background:'#f9f9f9',padding:16,borderRadius:8,marginTop:16}}>{JSON.stringify(result, null, 2)}</pre>}
      <Snackbar open={!!snackbar} autoHideDuration={3000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Paper>
  );
}
