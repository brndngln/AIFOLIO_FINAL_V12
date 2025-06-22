import React, { useEffect, useState } from 'react';
import axios from 'axios';

const VaultDropCountdownPanel = () => {
  const [countdown, setCountdown] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCountdown = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/sim/vault-drop-countdown', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setCountdown(res.data);
        setError(null);
      } catch (err) {
        setError('Error fetching countdown');
      }
      setLoading(false);
    };
    fetchCountdown();
    const interval = setInterval(fetchCountdown, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="theme-card">Loading countdown...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;
  if (!countdown) return null;

  return (
    <div className="theme-card" style={{ background: 'var(--background)', color: 'var(--text)', boxShadow: 'var(--shadow-md)', borderRadius: 'var(--border-radius-lg)', padding: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
      <h3 style={{ color: 'var(--accent)' }}>Next Vault Drop</h3>
      <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '1rem 0', letterSpacing: '0.1em', transition: 'color 0.4s', color: countdown.glitch ? 'var(--secondary)' : 'var(--cta)' }}>
        {countdown.display}
      </div>
      {countdown.glitch && <div className="text-warning" style={{ fontStyle: 'italic', color: 'var(--warning)' }}>{countdown.glitch_message}</div>}
      <div style={{ marginTop: '1rem', fontSize: '1rem', color: 'var(--secondary)' }}>Vault: <span style={{ color: 'var(--cta)', fontWeight: 'bold' }}>{countdown.vault_name}</span></div>
    </div>
  );
};

export default VaultDropCountdownPanel;
