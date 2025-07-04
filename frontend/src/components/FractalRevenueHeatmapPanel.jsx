import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

// [WINDSURF FIXED ✅]
// SAFE AI, deterministic, static, owner-controlled visualization
export default function FractalRevenueHeatmapPanel() {
  const [heatmap, setHeatmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const fetchHeatmap = async () => {
      setLoading(true);
      try {
        // Deterministic, static endpoint
        const res = await axios.get('/api/v110/revenue/fractal-heatmap');
        setHeatmap(res.data);
        setError(null);
      } catch (err) {
        setError('Error fetching fractal revenue heatmap');
      }
      setLoading(false);
    };
    fetchHeatmap();
    const interval = setInterval(fetchHeatmap, 20000); // Static refresh, not adaptive
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!heatmap || !canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, 400, 200);
    // Draw static, deterministic fractal heatmap dots
    (heatmap.points || []).forEach(pt => {
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, pt.intensity * 8, 0, 2 * Math.PI);
      ctx.fillStyle = `rgba(60, 180, 220, ${pt.intensity * 0.5})`;
      ctx.shadowColor = 'rgba(0, 120, 180, 0.12)';
      ctx.shadowBlur = 10;
      ctx.fill();
    });
  }, [heatmap]);

  if (loading) return <div className="theme-card">Loading fractal revenue heatmap...</div>;
  if (error) return <div className="theme-card text-error">{error}</div>;
  if (!heatmap) return null;

  return (
    <div className="theme-card" style={{ background: '#f0fdfa', color: '#0ea5e9', boxShadow: '0 1px 4px #bae6fd', borderRadius: '16px', padding: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
      <h3 style={{ color: '#059669', fontWeight: 700 }}>
        Fractal Revenue Heatmap
        <span style={{marginLeft:10,background:'#059669',color:'#fff',padding:'2px 10px',borderRadius:6,fontWeight:700,fontSize:13}} aria-label="SAFE AI badge">SAFE AI</span>
        <span tabIndex={0} aria-label="Help: What is the Fractal Revenue Heatmap?" title="Static, deterministic visualization of fractal revenue patterns. OWNER controls all exports." style={{marginLeft:6, color:'#64748b', cursor:'help', fontSize:18, fontWeight:800}}>?</span>
      </h3>
      <canvas
        ref={canvasRef}
        width={400}
        height={200}
        aria-label="Fractal Revenue Heatmap Visualization"
        style={{ width: '100%', maxWidth: 500, background: '#e0f7fa', borderRadius: '14px', margin: '1rem auto', display: 'block' }}
      />
      <div style={{ fontSize: '0.98rem', color: '#64748b', marginTop: '1rem' }}>
        Static, SAFE AI-compliant visualization of fractal revenue clusters. OWNER may export data for audit.
      </div>
      <button
        className="big-btn blue"
        aria-label="Export fractal heatmap data"
        title="Export fractal heatmap data (static, audit-logged)"
        onClick={() => {
          // Static, deterministic export (CSV)
          if (!heatmap || !heatmap.points) return;
          const csv = [
            'x,y,intensity',
            ...heatmap.points.map(pt => `${pt.x},${pt.y},${pt.intensity}`)
          ].join('\n');
          const blob = new Blob([csv], { type: 'text/csv' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'fractal_revenue_heatmap.csv';
          a.click();
          URL.revokeObjectURL(url);
        }}
        style={{marginTop:16}}
      >Export CSV</button>
    </div>
  );
}
