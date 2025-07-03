import React, { useState } from 'react';
import { Switch, FormControlLabel, Tooltip, Button } from '@mui/material';

export default function IntegrationControls({ notificationPrefs, onPrefsChange, onRotateApiKey, onComplianceAudit }) {
  return (
    <div style={{padding:20}}>
      <h3>Integrations & Notifications</h3>
      <Tooltip title="Toggle Slack notifications for owner events.">
        <FormControlLabel
          control={<Switch checked={notificationPrefs.slack} onChange={e=>onPrefsChange({ ...notificationPrefs, slack: e.target.checked })} />}
          label="Slack"
        />
      </Tooltip>
      <Tooltip title="Toggle Discord notifications for owner events.">
        <FormControlLabel
          control={<Switch checked={notificationPrefs.discord} onChange={e=>onPrefsChange({ ...notificationPrefs, discord: e.target.checked })} />}
          label="Discord"
        />
      </Tooltip>
      <Tooltip title="Toggle Email notifications for owner events.">
        <FormControlLabel
          control={<Switch checked={notificationPrefs.email} onChange={e=>onPrefsChange({ ...notificationPrefs, email: e.target.checked })} />}
          label="Email"
        />
      </Tooltip>
      <div style={{marginTop:20}}>
        <Tooltip title="Rotate all API keys (owner only, static logic)"><Button variant="outlined" onClick={onRotateApiKey}>Rotate API Keys</Button></Tooltip>
        <Tooltip title="Run static compliance audit and export log."><Button variant="outlined" style={{marginLeft:10}} onClick={onComplianceAudit}>Compliance Audit</Button></Tooltip>
      </div>
    </div>
  );
}
