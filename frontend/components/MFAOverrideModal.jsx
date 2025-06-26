import React, { useState } from 'react';
import { Modal, Box, Typography, TextField, Button, Alert } from '@mui/material';

const MFAOverrideModal = ({ open, onClose, onSubmit, error, loading }) => {
  const [code, setCode] = useState('');
  const handleSubmit = () => {
    onSubmit(code);
    setCode('');
  };
  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{ p: 4, bgcolor: 'background.paper', borderRadius: 2, maxWidth: 400, mx: 'auto', mt: '20vh' }}>
        <Typography variant="h6" mb={2}>MFA Required for Manual Rotation</Typography>
        <TextField
          label="6-digit MFA Code"
          value={code}
          onChange={e => setCode(e.target.value)}
          fullWidth
          inputProps={{ maxLength: 6, inputMode: 'numeric', pattern: '[0-9]*' }}
          margin="normal"
        />
        {error && <Alert severity="error">{error}</Alert>}
        <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading || code.length !== 6} fullWidth>
          {loading ? 'Verifying...' : 'Submit'}
        </Button>
      </Box>
    </Modal>
  );
};
export default MFAOverrideModal;
