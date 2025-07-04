import React, { useState } from 'react';
import { Box, Typography, Paper, Button, Divider, Grid, TextField, Snackbar } from '@mui/material';
import IntegrationInstructionsIcon from '@mui/icons-material/IntegrationInstructions';

const integrations = [
  { label: 'Notion', endpoint: '/api/integrate/notion', fields: ['title', 'content'] },
  { label: 'Airtable', endpoint: '/api/integrate/airtable', fields: ['table', 'record'] },
  { label: 'Slack', endpoint: '/api/integrate/slack', fields: ['text'] },
  { label: 'SMS', endpoint: '/api/integrate/sms', fields: ['to', 'body'] },
  { label: 'Webhook', endpoint: '/api/integrate/webhook', fields: ['payload', 'endpoint'] },
  { label: 'SendGrid', endpoint: '/api/integrate/sendgrid', fields: ['to_email', 'subject', 'message'] },
  { label: 'Discord', endpoint: '/api/integrate/discord', fields: ['message'] },
  { label: 'Google Sheets', endpoint: '/api/integrate/googlesheets', fields: ['sheet_id', 'values'] },
  { label: 'Zapier', endpoint: '/api/integrate/zapier', fields: ['payload'] },
  { label: 'Stripe', endpoint: '/api/integrate/stripe', fields: [] },
  { label: 'Shopify', endpoint: '/api/integrate/shopify', fields: [] },
  { label: 'WooCommerce', endpoint: '/api/integrate/woocommerce', fields: [] },
  { label: 'Gumroad', endpoint: '/api/integrate/gumroad', fields: [] },
];

export default function EliteBusinessIntegrationsPanel() {
  const [form, setForm] = useState({});
  const [snackbar, setSnackbar] = useState('');

  const handleChange = (key, value) => {
    setForm(f => ({ ...f, [key]: value }));
  };

  const handleSend = async (integration) => {
    try {
      const payload = {};
      integration.fields.forEach(f => { payload[f] = form[`${integration.label}_${f}`] || ''; });
      const res = await fetch(integration.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) setSnackbar(`${integration.label} integration sent!`);
      else setSnackbar(`Failed to send to ${integration.label}`);
    } catch {
      setSnackbar(`Failed to send to ${integration.label}`);
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <IntegrationInstructionsIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Elite Business Integrations</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        {integrations.map((integration, idx) => (
          <Grid item xs={12} md={6} key={integration.label}>
            <Paper sx={{ p: 2, mb: 2 }}>
              <Typography variant="subtitle1">{integration.label}</Typography>
              {integration.fields.map(f => (
                <TextField
                  key={f}
                  label={f.charAt(0).toUpperCase() + f.slice(1)}
                  value={form[`${integration.label}_${f}`] || ''}
                  onChange={e => handleChange(`${integration.label}_${f}`, e.target.value)}
                  fullWidth
                  sx={{ mb: 1 }}
                />
              ))}
              <Button variant="contained" color="primary" onClick={() => handleSend(integration)} sx={{ mt: 1 }}>
                Send to {integration.label}
              </Button>
            </Paper>
          </Grid>
        ))}
      </Grid>
      <Snackbar open={!!snackbar} autoHideDuration={3000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Paper>
  );
}
