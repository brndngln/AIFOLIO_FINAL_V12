import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Table, TableHead, TableRow, TableCell, TableBody, Paper, Button, CircularProgress } from '@mui/material';

const AnomalyDrilldown = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/usage/anomalies').then(res => setAnomalies(res.data)).finally(() => setLoading(false));
  }, []);

  const handleSelect = (a) => setSelected(a);

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Anomaly Drilldown</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Timestamp</TableCell>
                <TableCell>Key</TableCell>
                <TableCell>Current</TableCell>
                <TableCell>Avg</TableCell>
                <TableCell>Factor</TableCell>
                <TableCell>Event</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {anomalies.map((a, i) => (
                <TableRow key={i} selected={selected === a}>
                  <TableCell>{a.timestamp}</TableCell>
                  <TableCell>{a.key}</TableCell>
                  <TableCell>{a.current}</TableCell>
                  <TableCell>{a.avg.toFixed(2)}</TableCell>
                  <TableCell>{a.factor.toFixed(2)}</TableCell>
                  <TableCell>{a.event}</TableCell>
                  <TableCell><Button size="small" onClick={()=>handleSelect(a)}>Details</Button></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      {selected && (
        <Box sx={{ mt: 2, p: 2, bgcolor: '#fff', borderRadius: 2 }}>
          <Typography variant="subtitle1">Anomaly Details</Typography>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{JSON.stringify(selected, null, 2)}</pre>
        </Box>
      )}
    </Box>
  );
};
export default AnomalyDrilldown;
