import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Select, MenuItem, Snackbar, IconButton } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import RefreshIcon from '@mui/icons-material/Refresh';

const ALL_ROLES = ['OWNER', 'AUDITOR', 'OPERATOR'];

const AdminRoleManager = () => {
  const [admins, setAdmins] = useState({});
  const [editing, setEditing] = useState({});
  const [snackbar, setSnackbar] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchAdmins = () => {
    setLoading(true);
    axios.get('/api/roles/list').then(res => setAdmins(res.data)).finally(() => setLoading(false));
  };

  useEffect(() => { fetchAdmins(); }, []);

  const handleRoleChange = (adminId, role) => {
    setEditing(edit => ({ ...edit, [adminId]: edit[adminId] ? [...edit[adminId], role] : [role] }));
  };

  const handleSave = (adminId) => {
    axios.post('/api/roles/set', { adminId, roles: editing[adminId] })
      .then(() => { setSnackbar('Roles updated.'); fetchAdmins(); })
      .catch(() => setSnackbar('Failed to update roles.'));
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>Admin Role Management</Typography>
        <IconButton onClick={fetchAdmins}><RefreshIcon /></IconButton>
      </Box>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Admin ID</TableCell>
              <TableCell>Roles</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(admins).map(adminId => (
              <TableRow key={adminId}>
                <TableCell>{adminId}</TableCell>
                <TableCell>
                  <Select
                    multiple
                    value={editing[adminId] || admins[adminId]}
                    onChange={e => setEditing(edit => ({ ...edit, [adminId]: e.target.value }))}
                    size="small"
                  >
                    {ALL_ROLES.map(role => (
                      <MenuItem key={role} value={role}>{role}</MenuItem>
                    ))}
                  </Select>
                </TableCell>
                <TableCell>
                  <Button variant="contained" size="small" color="primary" startIcon={<SaveIcon />} onClick={() => handleSave(adminId)}>
                    Save
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Snackbar open={!!snackbar} autoHideDuration={3000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Box>
  );
};
export default AdminRoleManager;
