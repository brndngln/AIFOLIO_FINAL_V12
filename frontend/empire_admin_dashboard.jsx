import React, { useEffect, useState } from 'react';
import './dashboard.css';

// --- V80 Components ---
function EmpireControlHUD({ stats }) {
  // stats: { automations, income, errors, efficiency }
  return (
    <div className="empire-hud">
      <div className="hud-block green">Automations: <b>{stats.automations}</b></div>
      <div className="hud-block blue">Income: <b>${stats.income}</b></div>
      <div className="hud-block red">Errors: <b>{stats.errors}</b></div>
      <div className="hud-block yellow">Efficiency: <b>{stats.efficiency}%</b></div>
    </div>
  );
}

function SmartButtonLayer({ onChoose }) {
  // onChoose: (mode) => void
  return (
    <div className="smart-btn-layer">
      <span>Choose:</span>
      <button onClick={() => onChoose('once')}>Accept Once</button>
      <button onClick={() => onChoose('always')}>Always</button>
      <button onClick={() => onChoose('queue')}>Safe Queue</button>
    </div>
  );
}

function OwnerIntentToggle({ intentMode, setIntentMode }) {
  return (
    <div className="intent-toggle">
      <span>Owner Intent:</span>
      <button className={intentMode === 'auto' ? 'active' : ''} onClick={() => setIntentMode('auto')}>Fully Automate</button>
      <button className={intentMode === 'oversight' ? 'active' : ''} onClick={() => setIntentMode('oversight')}>Oversight</button>
      <button className={intentMode === 'override' ? 'active' : ''} onClick={() => setIntentMode('override')}>Override</button>
    </div>
  );
}

function PreferencePane({ title, children, open, onToggle }) {
  return (
    <div className="pref-pane">
      <div className="pref-pane-header" onClick={onToggle}>
        <span>{open ? '▼' : '►'}</span> <b>{title}</b>
      </div>
      {open && <div className="pref-pane-content">{children}</div>}
    </div>
  );
}

function EmpireAdminDashboard() {
  const [logs, setLogs] = useState({});
  const [activeSection, setActiveSection] = useState('Vaults');
  const [safeMode, setSafeMode] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [pendingAction, setPendingAction] = useState(null);
  const [undoStack, setUndoStack] = useState([]);
  const [lastAction, setLastAction] = useState(null);

  // V80 state
  const [hudStats, setHudStats] = useState({ automations: 0, income: 0, errors: 0, efficiency: 100 });
  const [automationQueue, setAutomationQueue] = useState([]);
  const [automationTags, setAutomationTags] = useState({});
  const [automationGrouping, setAutomationGrouping] = useState({});
  const [auditTrail, setAuditTrail] = useState([]);
  const [snapshots, setSnapshots] = useState([]);
  const [outliers, setOutliers] = useState([]);
  const [intentMode, setIntentMode] = useState('oversight');
  const [openPanes, setOpenPanes] = useState({ Vaults: true, AI: false, Automation: false, Branding: false, Security: false });
  const [notificationMsg, setNotificationMsg] = useState('');
  const [notificationChannel, setNotificationChannel] = useState('slack');
  const [efficiency, setEfficiency] = useState(100);

  // PHASE 91–110 state
  const [licensingVaults, setLicensingVaults] = useState([]);
  const [licensingVariants, setLicensingVariants] = useState([]);
  const [licensees, setLicensees] = useState([]);
  const [roiRanks, setRoiRanks] = useState([]);
  const [revenueFunnels, setRevenueFunnels] = useState([]);
  const [combatVaults, setCombatVaults] = useState([]);
  const [strategistReport, setStrategistReport] = useState({});
  const [vaultAuditLog, setVaultAuditLog] = useState([]);
  const [vaultAuditSnapshots, setVaultAuditSnapshots] = useState([]);
  const [fractalHeatmap, setFractalHeatmap] = useState([]);
  const [activeTab, setActiveTab] = useState('Vaults');

  // Fetch V80 HUD stats
  useEffect(() => {
    fetch('/api/v80/hud_stats').then(res => res.json()).then(setHudStats);
    fetch('/api/v80/automation_queue').then(res => res.json()).then(data => {
      setAutomationQueue(data.queue || []);
      setAutomationTags(data.tags || {});
      setAutomationGrouping(data.grouping || {});
    });
    fetch('/api/v80/audit_trail').then(res => res.json()).then(data => setAuditTrail(data.audit_trail || []));
    fetch('/api/v80/snapshots').then(res => res.json()).then(data => setSnapshots(data.snapshots || []));
    fetch('/api/v80/intent_mode').then(res => res.json()).then(data => setIntentMode(data.mode));
    fetch('/api/v80/outliers').then(res => res.json()).then(data => setOutliers(data.outliers || []));
    fetch('/api/v80/efficiency').then(res => res.json()).then(data => setEfficiency(data.efficiency));
    fetch('/api/dashboard/logs').then(res => res.json()).then(data => setLogs(data));
    // PHASE 91–110: Load licensing, revenue, intelligence, audit
    fetch('/api/v110/licensing/scan', {method:'POST',headers:{'Content-Type':'application/json'},body:'[]'}).then(res=>res.json()).then(data=>setLicensingVaults(data.vaults||[]));
    fetch('/api/v110/licensing/licensees').then(res=>res.json()).then(data=>setLicensees(data.licensees||[]));
    fetch('/api/v110/intel/combat_ai', {method:'POST',headers:{'Content-Type':'application/json'},body:'[]'}).then(res=>res.json()).then(data=>setCombatVaults(data.vaults||[]));
    fetch('/api/v110/intel/strategist', {method:'POST',headers:{'Content-Type':'application/json'},body:'[]'}).then(res=>res.json()).then(data=>setStrategistReport(data.report||{}));
    fetch('/api/v110/audit/log').then(res=>res.json()).then(data=>setVaultAuditLog(data.vault_audit_log||[]));
    fetch('/api/v110/audit/snapshots').then(res=>res.json()).then(data=>setVaultAuditSnapshots(data.snapshots||[]));
  }, []);

  // Tag/group automation task
  const tagTask = (id, tag) => {
    fetch('/api/v80/tag_task', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, tag }) })
      .then(() => fetch('/api/v80/automation_queue').then(res => res.json()).then(data => {
        setAutomationTags(data.tags || {});
      }));
  };
  const groupTask = (id, group) => {
    fetch('/api/v80/group_task', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, group }) })
      .then(() => fetch('/api/v80/automation_queue').then(res => res.json()).then(data => {
        setAutomationGrouping(data.grouping || {});
      }));
  };

  // Set owner intent mode
  const handleSetIntentMode = (mode) => {
    fetch('/api/v80/intent_mode/set', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode }) })
      .then(() => setIntentMode(mode));
  };

  // Notify
  const sendNotification = () => {
    fetch('/api/v80/notify', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ channel: notificationChannel, message: notificationMsg }) })
      .then(() => setNotificationMsg(''));
  };

  // Rollback
  const handleRollback = (idx) => {
    fetch('/api/v80/rollback', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ snapshot_index: idx }) })
      .then(() => fetch('/api/v80/snapshots').then(res => res.json()).then(data => setSnapshots(data.snapshots || [])));
  };

  // Color code helper
  const getStatusColor = (status) => {
    if (status === 'safe' || status === 'good' || status === 'green') return '#27ae60';
    if (status === 'warning' || status === 'yellow' || status === 'review') return '#f4d03f';
    if (status === 'red' || status === 'danger' || status === 'needs owner action') return '#e74c3c';
    if (status === 'critical') return '#e74c3c';
    if (status === 'experimental') return '#f4d03f';
    if (status === 'safe') return '#27ae60';
    return '#2980b9';
  };

  // Example panel renderers (expand for each section)
  // Helper: fetch V70 logs (stub)
  const getV70Log = (engine) => logs[engine] || [];

  // --- PHASE 91–110: Licensing, Revenue, Intelligence, Audit Panels ---
  const renderLicensingPanel = () => (
    <div className="dashboard-panel">
      <h2>Licensing Control Panel</h2>
      <button className="big-btn blue" onClick={()=>setActiveTab('Licensee Manager')}>Licensee Manager</button>
      <button className="big-btn green" onClick={()=>setActiveTab('ROI Analyzer')}>ROI Analyzer</button>
      <button className="big-btn yellow" onClick={()=>setActiveTab('Fractal Revenue Heatmap')}>Fractal Revenue Heatmap</button>
      <h3>All Vaults</h3>
      <table className="automation-queue-table">
        <thead><tr><th>ID</th><th>Title</th><th>Niche</th><th>Value</th><th>Potential</th><th>Actions</th></tr></thead>
        <tbody>
          {licensingVaults.map((v, idx)=>(
            <tr key={idx}>
              <td>{v.id}</td><td>{v.title}</td><td>{v.niche}</td><td>{v.value}</td><td>{v.licensing_potential}</td>
              <td>
                <button onClick={()=>{
                  fetch('/api/v110/licensing/variant', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({vault_id:v.id})})
                    .then(()=>alert('Variant generated!'));
                }}>Gen Variant</button>
                <button onClick={()=>{
                  fetch('/api/v110/licensing/license', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({vault_id:v.id,user:'owner',mode:'public'})})
                    .then(()=>alert('Licensed Publicly!'));
                }}>License Publicly</button>
                <button onClick={()=>{
                  fetch('/api/v110/licensing/license', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({vault_id:v.id,user:'owner',mode:'whitelist'})})
                    .then(()=>alert('Whitelisted!'));
                }}>Whitelist</button>
                <button onClick={()=>{
                  fetch('/api/v110/licensing/license', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({vault_id:v.id,user:'owner',mode:'private_clone_only'})})
                    .then(()=>alert('Private Clone Only!'));
                }}>Private Clone Only</button>
                <button onClick={()=>{
                  fetch('/api/v110/licensing/partner', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({vault_id:v.id,user:'partner'})})
                    .then(()=>alert('PartnerVault Mode!'));
                }}>PartnerVault</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  const renderLicenseeManagerPanel = () => (
    <div className="dashboard-panel">
      <h2>Licensee Manager</h2>
      <table className="automation-queue-table">
        <thead><tr><th>Vault ID</th><th>User</th><th>Variant</th><th>Region</th><th>Earnings</th><th>Status</th></tr></thead>
        <tbody>
          {licensees.map((l, idx)=>(
            <tr key={idx}>
              <td>{l.vault_id}</td><td>{l.user}</td><td>{l.variant_id}</td><td>{l.region}</td><td>{l.earnings}</td><td>{l.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  const renderROIAnalyzerPanel = () => (
    <div className="dashboard-panel">
      <h2>Vault ROI Analyzer</h2>
      <table className="automation-queue-table">
        <thead><tr><th>Vault ID</th><th>Profit</th><th>Threat Level</th></tr></thead>
        <tbody>
          {combatVaults.map((v, idx)=>(
            <tr key={idx}>
              <td>{v.id}</td><td>{v.profit}</td><td>{v.threat_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  const renderFractalHeatmapPanel = () => (
    <div className="dashboard-panel">
      <h2>Fractal Revenue Heatmap</h2>
      <pre>{JSON.stringify(fractalHeatmap,null,2)}</pre>
    </div>
  );
  const renderStrategistPanel = () => (
    <div className="dashboard-panel">
      <h2>Empire Vault Strategist</h2>
      <pre>{JSON.stringify(strategistReport,null,2)}</pre>
    </div>
  );
  const renderVaultAuditPanel = () => (
    <div className="dashboard-panel">
      <h2>Vault Audit Log</h2>
      <pre style={{maxHeight:200,overflow:'auto',background:'#f8f8f8'}}>{JSON.stringify(vaultAuditLog.slice(-30),null,2)}</pre>
      <h3>Snapshots</h3>
      <ul>
        {vaultAuditSnapshots.map((snap,idx)=>(
          <li key={idx}><button onClick={()=>alert('Rollback not implemented in UI yet')}>Rollback to {snap.timestamp}</button></li>
        ))}
      </ul>
    </div>
  );

  const renderSection = () => {
    switch (activeTab) {
      case 'Licensing':
        return renderLicensingPanel();
      case 'Licensee Manager':
        return renderLicenseeManagerPanel();
      case 'ROI Analyzer':
        return renderROIAnalyzerPanel();
      case 'Fractal Revenue Heatmap':
        return renderFractalHeatmapPanel();
      case 'Strategist':
        return renderStrategistPanel();
      case 'Vault Audit':
        return renderVaultAuditPanel();
      case 'Vaults':
        return (
          <div className="dashboard-panel">
            <h2>Vault Dashboard</h2>
            <button className="big-btn green" onClick={() => handleAction('createVault', {})}>New Vault</button>
            <button className="big-btn yellow" onClick={() => handleAction('qaVault', {})}>QA Check</button>
            <button className="big-btn blue" onClick={() => handleAction('bundleVault', {})}>Bundle Builder</button>
            {/* V80 Automation Queue View */}
            <h3>Automation Queue</h3>
            <table className="automation-queue-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Task</th>
                  <th>Tag</th>
                  <th>Group</th>
                  <th>Controls</th>
                </tr>
              </thead>
              <tbody>
                {automationQueue.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.id || idx}</td>
                    <td>{item.task ? JSON.stringify(item.task) : ''}</td>
                    <td>
                      <select value={automationTags[item.id] || ''} onChange={e => tagTask(item.id, e.target.value)}>
                        <option value="">-</option>
                        <option value="safe">Safe</option>
                        <option value="critical">Critical</option>
                        <option value="experimental">Experimental</option>
                      </select>
                    </td>
                    <td>
                      <select value={automationGrouping[item.id] || ''} onChange={e => groupTask(item.id, e.target.value)}>
                        <option value="">-</option>
                        <option value="Growth">Growth</option>
                        <option value="Maintenance">Maintenance</option>
                        <option value="Cleanup">Cleanup</option>
                        <option value="Emergency">Emergency</option>
                      </select>
                    </td>
                    <td>
                      <button onClick={() => handleAction('cancelAutomation', { id: item.id })}>Cancel</button>
                      <button onClick={() => handleAction('pauseAutomation', { id: item.id })}>Pause</button>
                      <button onClick={() => handleAction('retryAutomation', { id: item.id })}>Retry</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{marginTop: '1rem'}}>
              <b>Efficiency Score:</b> <span style={{color: getStatusColor(efficiency > 90 ? 'safe' : (efficiency > 70 ? 'yellow' : 'red'))}}>{efficiency}%</span>
            </div>
            <div style={{marginTop: '1rem'}}>
              <b>Audit Trail:</b>
              <pre style={{maxHeight: 120, overflow: 'auto', background: '#f8f8f8'}}>{JSON.stringify(auditTrail.slice(-10), null, 2)}</pre>
              <b>Rollback Snapshots:</b>
              <ul>
                {snapshots.map((snap, idx) => (
                  <li key={idx}>
                    <button onClick={() => handleRollback(idx)}>Rollback to {snap.timestamp}</button>
                  </li>
                ))}
              </ul>
            </div>
            <div style={{marginTop: '1rem'}}>
              <b>Outliers:</b>
              <ul>
                {outliers.map((o, idx) => (
                  <li key={idx}>{o.metric}: {o.value} <span style={{color: getStatusColor('red')}}>OUTLIER</span></li>
                ))}
              </ul>
            </div>
            <div style={{marginTop: '1rem'}}>
              <b>Send Notification:</b>
              <select value={notificationChannel} onChange={e => setNotificationChannel(e.target.value)}>
                <option value="slack">Slack</option>
                <option value="email">Email</option>
                <option value="telegram">Telegram</option>
              </select>
              <input value={notificationMsg} onChange={e => setNotificationMsg(e.target.value)} placeholder="Message..." />
              <button onClick={sendNotification}>Send</button>
            </div>
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
            <div className="dashboard-panel">
              <h2>Zero-Click Automation Queue</h2>
              <button className="big-btn blue" onClick={() => handleAction('approveAllZeroClick', {})}>Approve All Batches</button>
              <ul>
                {getV70Log('ai_zero_click_automation_queue').map((entry, idx) => (
                  <li key={idx}><pre>{JSON.stringify(entry, null, 2)}</pre></li>
                ))}
              </ul>
            </div>
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
      // Fallback for unknown tabs: show Vaults panel
      // This must be the last case before default
      case undefined:
        return (
          <div className="dashboard-panel">
            <h2>Vault Dashboard</h2>
            <p>Unknown tab selected. Showing Vaults panel by default.</p>
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
        {/* V80 Empire Control HUD */}
        <EmpireControlHUD stats={hudStats} />
        {/* V80 Owner Intent Toggle */}
        <OwnerIntentToggle intentMode={intentMode} setIntentMode={setIntentMode} />
        {/* V80 Collapsible Preference Panes */}
        <div className="pref-panes">
          {['Vaults','AI','Automation','Branding','Security'].map(pane => (
            <PreferencePane
              key={pane}
              title={pane}
              open={openPanes[pane]}
              onToggle={() => setOpenPanes({...openPanes, [pane]: !openPanes[pane]})}
            >
              {/* Example: SmartButtonLayer inside each pane */}
              <SmartButtonLayer onChoose={mode => alert(`Chosen: ${mode} for ${pane}`)} />
              {/* Add more controls per pane as needed */}
            </PreferencePane>
          ))}
        </div>
        {/* Existing Section Render */}
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

