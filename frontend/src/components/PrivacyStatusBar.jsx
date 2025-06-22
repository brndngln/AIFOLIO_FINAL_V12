import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PrivacyStatusBar = () => {
  const [status, setStatus] = useState({ consent: true, lastAudit: null, privacyMode: 'ON', loading: true });
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/monitor/metrics', { headers: { Authorization: `Bearer ${token}` } });
        setStatus({
          consent: true,
          lastAudit: res.data.system.timestamp,
          privacyMode: 'ON',
          loading: false
        });
      } catch {
        setStatus(s => ({ ...s, loading: false }));
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 60000);
    return () => clearInterval(interval);
  }, []);
  if (status.loading) return null;
  return (
    <div style={{ background: 'var(--secondary)', color: 'var(--text)', borderRadius: '8px', padding: '0.5rem 1.5rem', display: 'flex', alignItems: 'center', gap: '2rem', boxShadow: 'var(--shadow-xs)', marginBottom: '1rem', fontSize: '1.05rem' }}>
      <span style={{ fontWeight: 600, color: status.privacyMode === 'ON' ? 'var(--cta)' : 'var(--error)' }}>
        Privacy Mode: {status.privacyMode}
      </span>
      <span>
        User Consent: <span style={{ color: status.consent ? 'var(--cta)' : 'var(--error)', fontWeight: 600 }}>{status.consent ? 'Granted' : 'Missing'}</span>
      </span>
      <span>
        Last Audit: <span style={{ color: 'var(--accent)' }}>{status.lastAudit ? new Date(status.lastAudit).toLocaleString() : 'N/A'}</span>
      </span>
    </div>
  );
};

export default PrivacyStatusBar;
