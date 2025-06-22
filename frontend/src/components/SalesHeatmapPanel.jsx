import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

const SalesHeatmapPanel = () => {
  const [heatmap, setHeatmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const fetchHeatmap = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/api/sim/sales-heatmap', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setHeatmap(res.data);
        setError(null);
      } catch (err) {
        setError('Error fetching heatmap');
      }
      setLoading(false);
    };
    fetchHeatmap();
    const interval = setInterval(fetchHeatmap, 15000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!heatmap || !canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, 320, 160);
    // Draw soft, matted heatmap dots
    heatmap.points.forEach(pt => {
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, pt.intensity * 6, 0, 2 * Math.PI);
      ctx.fillStyle = `rgba(186, 170, 142, ${pt.intensity * 0.6})`;
      ctx.shadowColor = 'rgba(90, 105, 90, 0.2)';
      ctx.shadowBlur = 8;
      ctx.fill();
    });
  }, [heatmap]);

  if (loading) return <div className="theme-card">Loading heatmap...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;
  if (!heatmap) return null;

  return (
    <div className="theme-card" style={{ background: 'var(--background)', color: 'var(--text)', boxShadow: 'var(--shadow-md)', borderRadius: 'var(--border-radius-lg)', padding: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
      <h3 style={{ color: 'var(--accent)' }}>Sales Heatmap</h3>
      <canvas ref={canvasRef} width={320} height={160} style={{ width: '100%', maxWidth: 400, background: 'var(--secondary)', borderRadius: '12px', margin: '1rem auto', display: 'block' }} />
      <div style={{ fontSize: '0.95rem', color: 'var(--secondary)', marginTop: '1rem' }}>Simulated, privacy-preserving sales activity visualization.</div>
    </div>
  );
};

export default SalesHeatmapPanel;
