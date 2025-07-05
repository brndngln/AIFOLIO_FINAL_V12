import React, { useEffect, useState } from 'react';
import axios from 'axios';

// [WINDSURF FIXED ✅]
const ComplianceRiskScoreWidget = () => {
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // Remove if not used in render or logic

  useEffect(() => {
    const fetchRisk = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/sim/compliance-risk-score', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setRisk(res.data);
        setError(null);
      } catch (err) {
        setError('Error fetching risk score');
      }
      setLoading(false);
    };
    fetchRisk();
    const interval = setInterval(fetchRisk, 15000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="theme-card">Loading compliance risk score...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;
  if (!risk) return null;

  return (
    <div className="theme-card" style={{ background: 'var(--background)', color: 'var(--text)', boxShadow: 'var(--shadow-md)', borderRadius: 'var(--border-radius-lg)', padding: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
      <h3 style={{ color: 'var(--accent)' }}>Compliance Risk Score</h3>
      <div style={{ margin: '1.5rem 0' }}>
        <svg width="120" height="120">
          <circle cx="60" cy="60" r="52" fill="none" stroke="var(--secondary)" strokeWidth="8" />
          <circle cx="60" cy="60" r="52" fill="none" stroke="var(--cta)" strokeWidth="8" strokeDasharray={326} strokeDashoffset={326 - (risk.score * 3.26)} style={{ transition: 'stroke-dashoffset 1s' }} />
          <text x="60" y="68" textAnchor="middle" fontSize="2.2rem" fill="var(--cta)" fontWeight="bold">{risk.score}</text>
        </svg>
      </div>
      <div style={{ fontSize: '1rem', color: 'var(--secondary)' }}>{risk.description || 'Risk level calculated from compliance pipeline.'}</div>
    </div>
  );
};

export default ComplianceRiskScoreWidget;
