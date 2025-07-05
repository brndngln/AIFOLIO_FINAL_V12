import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, Button, CircularProgress } from '@mui/material';

const AnomalyRootCausePanel = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    axios.get('/api/anomaly/root_cause').then(res => setResults(res.data)).finally(() => setLoading(false));
  }, []);

  const handleSelect = (idx) => setSelected(results[idx]);

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Anomaly Root Cause Analysis</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Timestamp</TableCell>
                <TableCell>Key</TableCell>
                <TableCell>Root Cause</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.map((r, i) => (
                <TableRow key={i}>
                  <TableCell>{r.anomaly.timestamp}</TableCell>
                  <TableCell>{r.anomaly.key}</TableCell>
                  <TableCell>{r.root_cause}</TableCell>
                  <TableCell><Button size="small" onClick={()=>handleSelect(i)}>Details</Button></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      {selected && (
        <Box sx={{ mt: 2, p: 2, bgcolor: '#fff', borderRadius: 2 }}>
          <Typography variant="subtitle1">Root Cause Details</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{JSON.stringify(selected, null, 2)}</pre>
        </Box>
      )}
    </Box>
  );
};
export default AnomalyRootCausePanel;
