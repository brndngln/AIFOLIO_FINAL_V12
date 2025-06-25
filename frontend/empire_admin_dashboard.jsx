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
    'Empire Value', 'Security', 'Multi-Platform', 'Prestige Brand', 'Global Risk', 'Dynasty',
    // V70 Phases:
    'Zero-Click Queue', 'Smart Suggest', 'Risk Tiering', 'Night Mode', 'Ultra-Safe Auto', 'Legacy Auto-Safe', 'Intent Engine', 'Simulator', 'Scaling Mode', 'Empire Companion'
  ];

  const sectionIcons = {
    'Vaults': '🗄️', 'Revenue': '💰', 'Partners': '🤝', 'Compliance': '📋', 'Capital': '🏦',
    'Crisis': '🚨', 'Empire Value': '🏆', 'Security': '🛡️', 'Multi-Platform': '🌐',
    'Prestige Brand': '✨', 'Global Risk': '🌎', 'Dynasty': '👑',
    'Zero-Click Queue': '⚡', 'Smart Suggest': '💡', 'Risk Tiering': '📊', 'Night Mode': '🌙', 'Ultra-Safe Auto': '🟢',
    'Legacy Auto-Safe': '🕰️', 'Intent Engine': '🎯', 'Simulator': '🧪', 'Scaling Mode': '📈', 'Empire Companion': '🤖'
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
  // Helper: fetch V70 logs (stub)
  const getV70Log = (engine) => logs[engine] || [];

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
      case 'Zero-Click Queue':
        return (
          <div className="dashboard-panel">
            <h2>Zero-Click Automation Queue</h2>
            <button className="big-btn blue" onClick={() => handleAction('approveAllZeroClick', {})}>Approve All Batches</button>
            <ul>
              {getV70Log('ai_zero_click_automation_queue').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Smart Suggest':
        return (
          <div className="dashboard-panel">
            <h2>Smart Suggest Mode</h2>
            <button className="big-btn green" onClick={() => handleAction('acceptAllSmartSuggest', {})}>Accept All Suggestions</button>
            <ul>
              {getV70Log('ai_smart_suggest_mode').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Risk Tiering':
        return (
          <div className="dashboard-panel">
            <h2>Dynamic Risk Tiering</h2>
            <button className="big-btn yellow" onClick={() => handleAction('autoApproveLowRisk', {})}>Auto-Approve Low Risk</button>
            <ul>
              {getV70Log('ai_dynamic_risk_tiering').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Night Mode':
        return (
          <div className="dashboard-panel">
            <h2>Night-Mode Automations</h2>
            <button className="big-btn blue" onClick={() => handleAction('scheduleNightRun', {})}>Schedule Overnight Run</button>
            <ul>
              {getV70Log('ai_night_mode_automations').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Ultra-Safe Auto':
        return (
          <div className="dashboard-panel">
            <h2>Ultra-Safe Auto Mode</h2>
            <button className="big-btn green" onClick={() => handleAction('runUltraSafe', {})}>Run Ultra-Safe Automations</button>
            <ul>
              {getV70Log('ai_ultra_safe_auto_mode').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Legacy Auto-Safe':
        return (
          <div className="dashboard-panel">
            <h2>Legacy Auto-Safe Mode</h2>
            <button className="big-btn blue" onClick={() => handleAction('activateLegacyAuto', {})}>Activate Legacy Auto-Safe</button>
            <ul>
              {getV70Log('ai_legacy_auto_safe_mode').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Intent Engine':
        return (
          <div className="dashboard-panel">
            <h2>Owner Intent Engine</h2>
            <button className="big-btn green" onClick={() => handleAction('autoAcceptIntent', {})}>Auto-Accept Common Actions</button>
            <ul>
              {getV70Log('ai_owner_intent_engine').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Simulator':
        return (
          <div className="dashboard-panel">
            <h2>Full Business Simulator</h2>
            <button className="big-btn yellow" onClick={() => handleAction('simulateAll', {})}>Preview All Automations</button>
            <ul>
              {getV70Log('ai_full_business_simulator').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Scaling Mode':
        return (
          <div className="dashboard-panel">
            <h2>Scheduled Scaling Mode</h2>
            <button className="big-btn blue" onClick={() => handleAction('setScalingTarget', {})}>Set Scaling Target</button>
            <button className="big-btn green" onClick={() => handleAction('approveCheckpoint', {})}>Approve Checkpoint</button>
            <ul>
              {getV70Log('ai_scheduled_scaling_mode').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
          </div>
        );
      case 'Empire Companion':
        return (
          <div className="dashboard-panel">
            <h2>Personal Empire Companion</h2>
            <button className="big-btn green" onClick={() => handleAction('generateBrief', {})}>Generate Daily Brief</button>
            <ul>
              {getV70Log('ai_personal_empire_companion').map((entry, idx) => (
                <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
              ))}
            </ul>
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
