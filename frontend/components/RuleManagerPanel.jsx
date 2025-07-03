import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, Button, TextField, Dialog, DialogTitle, DialogContent, DialogActions, Snackbar, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const RuleManagerPanel = () => {
  const [rules, setRules] = useState({});
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [platform, setPlatform] = useState('');
  const [pattern, setPattern] = useState('');
  const [desc, setDesc] = useState('');
  const [severity, setSeverity] = useState('major');
  const [law, setLaw] = useState('');
  const [snackbar, setSnackbar] = useState('');

  useEffect(()=>{ fetchRules(); },[]);

  const fetchRules = () => {
    axios.get('/api/rules/get').then(res=>setRules(res.data));
  };
  const handleOpen = (p, r) => {
    setEditing({p,r});
    setPlatform(p);
    setPattern(r.pattern);
    setDesc(r.desc);
    setSeverity(r.severity);
    setLaw(r.law);
    setOpen(true);
  };
  const handleSave = () => {
    const payload = { platform, pattern, desc, severity, law };
    if (editing) payload.edit = true;
    axios.post('/api/rules/update', payload)
      .then(()=>{ setOpen(false); setSnackbar('Rule saved!'); fetchRules(); })
      .catch(()=>setSnackbar('Save failed.'));
  };
  const handleDelete = (p, r) => {
    axios.post('/api/rules/delete', { platform: p, pattern: r.pattern })
      .then(()=>{ setSnackbar('Rule deleted!'); fetchRules(); })
      .catch(()=>setSnackbar('Delete failed.'));
  };
  return (
    <Box sx={{ p: 3, bgcolor: '#f8f8f8', borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>Detection Rule Manager</Typography>
      <Button variant="contained" color="primary" onClick={()=>{setEditing(null);setPlatform('');setPattern('');setDesc('');setSeverity('major');setLaw('');setOpen(true);}}>Add Rule</Button>
      <Paper sx={{mt:2}}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Platform</TableCell>
              <TableCell>Pattern</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Law</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(rules).flatMap(([p, arr]) => arr.map((r, i) => (
              <TableRow key={p+i}>
                <TableCell>{p}</TableCell>
                <TableCell>{r.pattern}</TableCell>
                <TableCell>{r.desc}</TableCell>
                <TableCell>{r.severity}</TableCell>
                <TableCell>{r.law}</TableCell>
                <TableCell>
                  <Button size="small" onClick={()=>handleOpen(p, r)}>Edit</Button>
                  <IconButton size="small" onClick={()=>handleDelete(p, r)}><DeleteIcon /></IconButton>
                </TableCell>
              </TableRow>
            )))}
          </TableBody>
        </Table>
      </Paper>
      <Dialog open={open} onClose={()=>setOpen(false)}>
        <DialogTitle>{editing?'Edit':'Add'} Rule</DialogTitle>
        <DialogContent>
          <TextField label="Platform" value={platform} onChange={e=>setPlatform(e.target.value)} fullWidth sx={{mb:2}} />
          <TextField label="Pattern" value={pattern} onChange={e=>setPattern(e.target.value)} fullWidth sx={{mb:2}} />
          <TextField label="Description" value={desc} onChange={e=>setDesc(e.target.value)} fullWidth sx={{mb:2}} />
          <TextField label="Severity" value={severity} onChange={e=>setSeverity(e.target.value)} fullWidth sx={{mb:2}} />
          <TextField label="Law" value={law} onChange={e=>setLaw(e.target.value)} fullWidth sx={{mb:2}} />
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>setOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
      <Snackbar open={!!snackbar} autoHideDuration={4000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Box>
  );
};
export default RuleManagerPanel;
