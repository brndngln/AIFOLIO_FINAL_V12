import React from 'react';
import { Switch, FormControlLabel } from '@mui/material';

export default function EliteThemeToggle({ darkMode, onToggle }) {
  return (
    <FormControlLabel
      control={<Switch checked={darkMode} onChange={onToggle} />}
      label={darkMode ? 'Dark Mode' : 'Light Mode'}
    />
  );
}
