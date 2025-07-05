import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress, Alert } from '@mui/material';

const RemediationRecommendationsPanel = () => {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/compliance/remediation').then(res => setRecs(res.data)).finally(() => setLoading(false));
  }, []);

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Automated Remediation Recommendations</Typography>
      {loading ? <CircularProgress /> : recs.length === 0 ? <Alert severity="success">No remediation required. All controls covered!</Alert> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Standard</TableCell>
                <TableCell>Control</TableCell>
                <TableCell>Recommendation</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {recs.map((r, i) => (
                <TableRow key={i}>
                  <TableCell>{r.standard}</TableCell>
                  <TableCell>{r.control}</TableCell>
                  <TableCell>{r.recommendation}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
};
export default RemediationRecommendationsPanel;
