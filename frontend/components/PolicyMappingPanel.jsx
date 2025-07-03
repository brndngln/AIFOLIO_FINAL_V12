import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress } from '@mui/material';

const PolicyMappingPanel = () => {
  const [mappings, setMappings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/policy/mapping').then(res => setMappings(res.data)).finally(() => setLoading(false));
  }, []);

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Policy Mapping to External Standards</Typography>
      {loading ? <CircularProgress /> : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Policy Type</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>ISO 27001</TableCell>
                <TableCell>NIST 800-53</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mappings.map((m, i) => (
                <TableRow key={i}>
                  <TableCell>{m.policy.type}</TableCell>
                  <TableCell>{m.policy.description}</TableCell>
                  <TableCell>{m.external_mapping.iso27001}</TableCell>
                  <TableCell>{m.external_mapping.nist80053}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  );
};
export default PolicyMappingPanel;
