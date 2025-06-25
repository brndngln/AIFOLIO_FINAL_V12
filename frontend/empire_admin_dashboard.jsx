import React, { useEffect, useState } from 'react';
import './dashboard.css';

function EmpireAdminDashboard() {
  const [logs, setLogs] = useState({});
  const [activeSection, setActiveSection] = useState('Vaults');
  const [safeMode, setSafeMode] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);
  const [undoStack, setUndoStack] = useState([]);
  const [lastAction, setLastAction] = useState(null);

  useEffect(() => {
    fetch('/api/dashboard/logs')
      .then(res => res.json())
      .then(data => setLogs(data));
  }, []);

  const sections = [
    'Vaults', 'Revenue', 'Partners', 'Compliance', 'Capital', 'Crisis',
    'Empire Value', 'Security', 'Multi-Platform', 'Prestige Brand', 'Global Risk', 'Dynasty'
  ];

  const sectionIcons = {
    'Vaults': '🗄️', 'Revenue': '💰', 'Partners': '🤝', 'Compliance': '📋', 'Capital': '🏦',
    'Crisis': '🚨', 'Empire Value': '🏆', 'Security': '🛡️', 'Multi-Platform': '🌐',
    'Prestige Brand': '✨', 'Global Risk': '🌎', 'Dynasty': '👑'
  };

  const handleAction = (action, details) => {
    setShowConfirm(true);
    setPendingAction({ action, details });
  };

  const confirmAction = () => {
    setUndoStack([...undoStack, lastAction]);
    setLastAction(pendingAction);
    setShowConfirm(false);
    setPendingAction(null);
    // Here you would call the backend API to perform the action
  };

  const undoAction = () => {
    if (undoStack.length === 0) return;
    const prev = undoStack[undoStack.length - 1];
    setUndoStack(undoStack.slice(0, -1));
    setLastAction(prev);
    // Here you would call the backend API to undo
  };

  // Color code helper
  const getStatusColor = (status) => {
    if (status === 'safe' || status === 'good' || status === 'green') return '#27ae60';
    if (status === 'warning' || status === 'yellow' || status === 'review') return '#f4d03f';
    if (status === 'red' || status === 'danger' || status === 'needs owner action') return '#e74c3c';
    return '#2980b9';
  };

  // Example panel renderers (expand for each section)
  const renderSection = () => {
    switch (activeSection) {
      case 'Vaults':
        return (
          <div className="dashboard-panel">
            <h2>Vault Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('createVault', {})}>New Vault</button>
            <button className="big-btn yellow" onClick={() => handleAction('qaVault', {})}>QA Check</button>
            <button className="big-btn blue" onClick={() => handleAction('bundleVault', {})}>Bundle Builder</button>
            {/* Visual previews, status bars, etc. */}
          </div>
        );
      case 'Revenue':
        return (
          <div className="dashboard-panel">
            <h2>Revenue Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('suggestPricing', {})}>Pricing Suggestions</button>
            <button className="big-btn blue" onClick={() => handleAction('subscriptionBundles', {})}>Subscription Bundles</button>
          </div>
        );
      case 'Partners':
        return (
          <div className="dashboard-panel">
            <h2>Partner Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('prospectPartners', {})}>Partner Candidates</button>
            <button className="big-btn blue" onClick={() => handleAction('licensingOffers', {})}>Licensing Offers</button>
          </div>
        );
      case 'Compliance':
        return (
          <div className="dashboard-panel">
            <h2>Compliance Center</h2>
            <div className="status-indicator" style={{background: getStatusColor('green')}}>IP Alerts: Safe</div>
            <div className="status-indicator" style={{background: getStatusColor('yellow')}}>Legal Updates: Review</div>
            <div className="status-indicator" style={{background: getStatusColor('red')}}>Owner Action Needed</div>
          </div>
        );
      case 'Capital':
        return (
          <div className="dashboard-panel">
            <h2>Capital Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('cashflow', {})}>View Cashflow</button>
            <button className="big-btn blue" onClick={() => handleAction('wealthFunnel', {})}>Wealth Funnel</button>
          </div>
        );
      case 'Crisis':
        return (
          <div className="dashboard-panel">
            <h2>Crisis Center</h2>
            <button className="big-btn red" onClick={() => handleAction('crisisMode', {})}>Activate Crisis Mode</button>
          </div>
        );
      case 'Empire Value':
        return (
          <div className="dashboard-panel">
            <h2>Empire Value Center</h2>
            <button className="big-btn green" onClick={() => handleAction('valuation', {})}>Current Valuation</button>
            <button className="big-btn blue" onClick={() => handleAction('improveValue', {})}>Improve Value</button>
          </div>
        );
      case 'Security':
        return (
          <div className="dashboard-panel">
            <h2>Security Center</h2>
            <button className="big-btn yellow" onClick={() => handleAction('antiFraud', {})}>Anti-Fraud</button>
            <button className="big-btn blue" onClick={() => handleAction('antiPiracy', {})}>Anti-Piracy</button>
            <button className="big-btn red" onClick={() => handleAction('shieldStatus', {})}>Shield Status</button>
          </div>
        );
      case 'Multi-Platform':
        return (
          <div className="dashboard-panel">
            <h2>Multi-Platform Dashboard</h2>
            <button className="big-btn blue" onClick={() => handleAction('syncAll', {})}>Sync All</button>
          </div>
        );
      case 'Prestige Brand':
        return (
          <div className="dashboard-panel">
            <h2>Prestige Brand Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('brandSuggestions', {})}>Brand Suggestions</button>
            <button className="big-btn yellow" onClick={() => handleAction('approveStyle', {})}>Approve Style Changes</button>
          </div>
        );
      case 'Global Risk':
        return (
          <div className="dashboard-panel">
            <h2>Global Risk Center</h2>
            <div className="status-indicator" style={{background: getStatusColor('green')}}>Macro Risks: Safe</div>
            <div className="status-indicator" style={{background: getStatusColor('yellow')}}>Platform Risks: Review</div>
            <div className="status-indicator" style={{background: getStatusColor('red')}}>AI Regulation: Owner Action Needed</div>
          </div>
        );
      case 'Dynasty':
        return (
          <div className="dashboard-panel">
            <h2>Dynasty Center</h2>
            <button className="big-btn green" onClick={() => handleAction('trustStatus', {})}>Family Trust Status</button>
            <button className="big-btn blue" onClick={() => handleAction('exportPlaybook', {})}>Export Dynasty Playbook</button>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="dashboard-flex">
      {/* Sidebar Navigation */}
      <nav className="dashboard-sidebar">
        <div className="sidebar-title">AIFOLIO™</div>
        {sections.map(section => (
          <div
            key={section}
            className={`sidebar-item${activeSection === section ? ' active' : ''}`}
            onClick={() => setActiveSection(section)}
          >
            <span className="sidebar-icon">{sectionIcons[section]}</span>
            {section}
          </div>
        ))}
        <div className="sidebar-safe-mode">
          <label>
            <input
              type="checkbox"
              checked={safeMode}
              onChange={() => setSafeMode(!safeMode)}
            />
            Safe Mode
          </label>
        </div>
      </nav>
      {/* Main Panel */}
      <main className="dashboard-main">
        {renderSection()}
        {/* Memory Audit & Last AI Action Log */}
        <div className="dashboard-memory-audit">
          <h3>Memory Audit Panel</h3>
          <pre>{JSON.stringify(logs, null, 2)}</pre>
        </div>
        <div className="dashboard-last-action">
          <h3>Last AI Action</h3>
          <pre>{JSON.stringify(lastAction, null, 2)}</pre>
        </div>
        {/* Undo Button */}
        <button className="big-btn yellow" onClick={undoAction} disabled={undoStack.length === 0}>Undo</button>
      </main>
      {/* Confirm Dialog */}
      {showConfirm && (
        <div className="dashboard-confirm-dialog">
          <div className="confirm-dialog-content">
            <h2>Confirm Action</h2>
            <p>Are you sure you want to proceed with this action?</p>
            <button className="big-btn green" onClick={confirmAction}>Yes, Approve</button>
            <button className="big-btn red" onClick={() => setShowConfirm(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}


export default EmpireAdminDashboard;
