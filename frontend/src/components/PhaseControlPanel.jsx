import React, { useEffect, useState } from 'react';
import './PhaseControlPanel.css';

const API = {
  status: '/api/phase/status',
  triggerUpgrade: '/api/phase/trigger-upgrade',
  toggleSafeMode: '/api/phase/safe-mode',
  lockdown: '/api/phase/lockdown',
};

export default function PhaseControlPanel() {
  const [phase, setPhase] = useState('');
  const [safeMode, setSafeMode] = useState('');
  const [lastUpgrade, setLastUpgrade] = useState('');
  const [nextUpgrade, setNextUpgrade] = useState('');
  const [systemIntegrity, setSystemIntegrity] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchStatus = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(API.status);
      const data = await res.json();
      setPhase(data.phase);
      setSafeMode(data.safe_mode);
      setLastUpgrade(data.last_upgrade);
      setNextUpgrade(data.next_upgrade);
      setSystemIntegrity(data.system_integrity);
    } catch (e) { // [WINDSURF FIXED]
      setError('Failed to fetch status.');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleUpgrade = async () => {
    setLoading(true);
    setError('');
    try {
      await fetch(API.triggerUpgrade, { method: 'POST' });
      fetchStatus();
    } catch (e) { // [WINDSURF FIXED]
      setError('Failed to trigger upgrade.');
    }
    setLoading(false);
  };

  const handleSafeMode = async () => {
    setLoading(true);
    setError('');
    try {
      await fetch(API.toggleSafeMode, { method: 'POST' });
      fetchStatus();
    } catch (e) { // [WINDSURF FIXED]
      setError('Failed to toggle safe mode.');
    }
    setLoading(false);
  };

  const handleLockdown = async () => {
    setLoading(true);
    setError('');
    try {
      await fetch(API.lockdown, { method: 'POST' });
      fetchStatus();
    } catch (e) { // [WINDSURF FIXED]
      setError('Failed to lockdown system.');
    }
    setLoading(false);
  };

  return (
    <div className="phase-control-panel">
      <h2>PHASE CONTROL PANEL</h2>
      <div className="phase-panel-buttons">
        <button onClick={fetchStatus} disabled={loading}>CHECK CURRENT PHASE STATUS</button>
        <button onClick={handleSafeMode} disabled={loading}>
          TOGGLE SAFE MODE [{safeMode === 'ON' ? 'ON' : 'OFF'}]
        </button>
        <button onClick={handleUpgrade} disabled={loading}>TRIGGER FULL UPGRADE NOW</button>
        <button className="lockdown" onClick={handleLockdown} disabled={loading}>LOCKDOWN SYSTEM NOW (EMERGENCY)</button>
      </div>
      <div className="phase-panel-status">
        <div><strong>Current Phase:</strong> {phase}</div>
        <div><strong>Safe Mode:</strong> {safeMode}</div>
        <div><strong>Last Upgrade:</strong> {lastUpgrade}</div>
        <div><strong>Next Scheduled Upgrade:</strong> {nextUpgrade}</div>
        <div><strong>System Integrity:</strong> {systemIntegrity}</div>
      </div>
      {error && <div className="phase-panel-error">{error}</div>}
    </div>
  );
}
