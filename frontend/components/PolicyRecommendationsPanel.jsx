import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress, Button, Snackbar } from '@mui/material';

const PolicyRecommendationsPanel = ({ onAddPolicy }) => {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState('');

  useEffect(() => {
    axios.get('/api/policy/recommend').then(res => setRecs(res.data)).finally(() => setLoading(false));
  }, []);

  const handleAdd = (rec) => {
    axios.post('/api/policy/add', { policy: rec })
      .then(() => { setSnackbar('Policy added.'); if (onAddPolicy) onAddPolicy(); })
      .catch(() => setSnackbar('Add failed.'));
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Automated Compliance Policy Recommendations</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Type</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Block?</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {recs.map((rec, i) => (
                <TableRow key={i}>
                  <TableCell>{rec.type}</TableCell>
                  <TableCell>{rec.description}</TableCell>
                  <TableCell>{rec.block ? 'Block' : 'Allow'}</TableCell>
                  <TableCell><Button size="small" variant="contained" onClick={()=>handleAdd(rec)}>Add Policy</Button></TableCell>
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
export default PolicyRecommendationsPanel;
