import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AILogVisualizerPanel = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/sim/ai-log-visualizer', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setLogs(res.data.logs || []);
        setError(null);
      } catch (err) {
        setError('Error fetching AI logs');
      }
      setLoading(false);
    };
    fetchLogs();
    const interval = setInterval(fetchLogs, 8000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="theme-card">Loading AI logs...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;
  if (!logs.length) return <div className="theme-card">No recent AI activity.</div>;

  return (
    <div className="theme-card" style={{ background: 'var(--background)', color: 'var(--text)', boxShadow: 'var(--shadow-md)', borderRadius: 'var(--border-radius-lg)', padding: '2rem', marginBottom: '2rem' }}>
      <h3 style={{ color: 'var(--accent)' }}>AI Log Visualizer</h3>
      <div style={{ maxHeight: 240, overflowY: 'auto', marginTop: '1rem' }}>
        {logs.map((entry, i) => (
          <div key={i} style={{ background: 'var(--secondary)', borderRadius: '8px', padding: '0.75rem 1rem', marginBottom: '0.5rem', boxShadow: 'var(--shadow-xs)', color: entry.status === 'WARNING_SIM' ? 'var(--warning)' : entry.status === 'ERROR_SIM' ? 'var(--error)' : 'var(--text)' }}>
            <div style={{ fontWeight: 600 }}>{entry.message || entry.log_id_sim}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--cta)' }}>{entry.timestamp_sim || entry.timestamp}</div>
            {entry.status && <span style={{ fontSize: '0.8rem', fontWeight: 500 }}>{entry.status}</span>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AILogVisualizerPanel;
