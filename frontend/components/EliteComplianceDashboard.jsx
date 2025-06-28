import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box, Typography, Grid, Paper, Button, Chip, Table, TableHead, TableRow, TableCell, TableBody, CircularProgress, Select, MenuItem, InputLabel, FormControl, Snackbar, Tabs, Tab
} from '@mui/material';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import ReplayIcon from '@mui/icons-material/Replay';
import EditIcon from '@mui/icons-material/Edit';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import FlashOnIcon from '@mui/icons-material/FlashOn';
import EliteAIAnalyticsPanel from './EliteAIAnalyticsPanel';
import EliteKPIDashboard from './EliteKPIDashboard';
import EliteRuleEditor from './EliteRuleEditor';
import EliteAlertRoutingPanel from './EliteAlertRoutingPanel';
import EliteDrilldownModal from './EliteDrilldownModal';
import EliteThemeToggle from './EliteThemeToggle';
import EliteGamificationPanel from './EliteGamificationPanel';
import EliteExportPanel from './EliteExportPanel';
import EliteAuditSimulationPanel from './EliteAuditSimulationPanel';
import EliteSAFEAIScorePanel from './EliteSAFEAIScorePanel';
import EliteBusinessIntegrationsPanel from './EliteBusinessIntegrationsPanel';
import EliteAdvancedAnalyticsPanel from './EliteAdvancedAnalyticsPanel';
// --- Extension Point: Import future elite analytics panels here ---
import EliteSecurityPerformancePanel from './EliteSecurityPerformancePanel';
import EliteComplianceExportsPanel from './EliteComplianceExportsPanel';
import EliteHeartbeatPanel from './EliteHeartbeatPanel';

const API_URL = '/api/compliance'; // Backend endpoint for compliance events

const statusColors = {
  ok: 'success',
  warning: 'warning',
  danger: 'error',
  escalated: 'secondary',
  critical: 'error',
  major: 'warning',
  minor: 'info',
  info: 'default',
};

function maskReviewer(id) {
  if (!id) return '';
  return id.slice(0,2) + '***' + id.slice(-2);
}

const EliteComplianceDashboard = () => {
  const [tab, setTab] = useState(0);
  // --- Extension Point: Add state for future analytics modules here ---
  const [drilldownOpen, setDrilldownOpen] = useState(false);
  const [drilldownEvent, setDrilldownEvent] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [rules, setRules] = useState('');
  const [alertRoutes, setAlertRoutes] = useState([]);
  const [kpiData, setKpiData] = useState(null);
  const [safeaiScore, setSafeaiScore] = useState({score:98,details:{}});
  const [marketTrends, setMarketTrends] = useState(null);
  const [engagement, setEngagement] = useState(null);
  const [lifecycle, setLifecycle] = useState(null);
  const [profitability, setProfitability] = useState(null);
  const [bundles, setBundles] = useState(null);
  const [anomaly, setAnomaly] = useState(null);
  const [aiQuality, setAiQuality] = useState(null);

  // Fetch rules, alert routes, KPI, SAFE AI score, and all elite analytics on mount
  useEffect(() => {
    axios.get('/api/rules/get').then(r => setRules(JSON.stringify(r.data, null, 2)));
    axios.get('/api/alert/routes').then(r => setAlertRoutes(r.data));
    axios.get('/api/kpi/elite').then(r => setKpiData(r.data));
    axios.get('/api/safeai/score').then(r => setSafeaiScore(r.data));
    axios.get('/api/trends/marketplace').then(r => setMarketTrends(r.data));
    axios.get('/api/lifecycle/summary').then(r => setLifecycle(r.data));
    // Simulate engagement, profitability, bundles, anomaly, ai quality fetch (owner can wire in real data)
    axios.get('/api/engagement/calculate?vault_id=vault_001').then(r => setEngagement(r.data));
    axios.post('/api/profitability/calculate', {vault_id:'vault_001',sales:[],refunds:[],costs:[]}).then(r=>setProfitability(r.data));
    axios.post('/api/bundles/recommend', {vault_id:'vault_001',purchase_history:[]}).then(r=>setBundles(r.data));
    axios.post('/api/anomaly/sales', {vault_id:'vault_001',sales:[]}).then(r=>setAnomaly(r.data));
    axios.post('/api/aiquality/quality', {text:'Elite test string'}).then(r=>setAiQuality(r.data));
  }, []);

  // Drilldown handler
  const handleDrilldown = (event) => {
    setDrilldownEvent(event);
    setDrilldownOpen(true);
  };

  // Save rules
  const handleSaveRules = (newRules) => {
    setRules(newRules);
    axios.post('/api/rules/update', { rules: JSON.parse(newRules) }).then(() => setSnackbar('Rules updated!')).catch(()=>setSnackbar('Rule update failed.'));
  };

  // Save alert routes
  const handleSaveRoutes = (routes) => {
    setAlertRoutes(routes);
    axios.post('/api/alert/routes', { routes }).then(() => setSnackbar('Alert routes updated!')).catch(()=>setSnackbar('Alert route update failed.'));
  };

  // Export handler
  const handleEliteExport = (type) => {
    setSnackbar('Exporting...');
    axios.get(`/api/export/${type}`).then(res => setSnackbar('Exported!')).catch(()=>setSnackbar('Export failed.'));
  };

  // Audit simulation handler
  const handleSimulateAudit = (reviewer, vault) => {
    setSnackbar('Simulating audit...');
    axios.post('/api/audit/simulate', { reviewer, vault }).then(()=>setSnackbar('Audit simulation complete!')).catch(()=>setSnackbar('Simulation failed.'));
  };

  const [violations, setViolations] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [vaultFilter, setVaultFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState('');

  useEffect(() => {
    fetchAll();
  }, []);


  const fetchAll = () => {
    setLoading(true);
    Promise.all([
      axios.get('/api/compliance/violations'),
      axios.get('/api/reviewer/leaderboard')
    ]).then(([v, l]) => {
      setViolations(v.data);
      setLeaderboard(l.data);
    }).finally(() => setLoading(false));
  };

  const handleExport = (type, docId) => {
    setSnackbar('Exporting...');
    axios.get(`/api/report/export_${type}${docId ? `?doc_id=${docId}` : ''}`)
      .then(res => {
        setSnackbar(`Exported: ${res.data.file || 'Ready for download'}`);
      })
      .catch(() => setSnackbar('Export failed.'));
  };

  const handleRemediate = (idx) => {
    axios.post('/api/remediation/apply', { idx, admin_id: 'admin' })
      .then(() => { setSnackbar('Remediation applied!'); fetchAll(); })
      .catch(() => setSnackbar('Remediation failed.'));
  };

  const handleRollback = (idx) => {
    axios.post('/api/remediation/rollback', { idx })
      .then(() => { setSnackbar('Remediation rolled back!'); fetchAll(); })
      .catch(() => setSnackbar('Rollback failed.'));
  };

  const filtered = violations.filter(v =>
    (statusFilter === 'all' || v.status === statusFilter) &&
    (severityFilter === 'all' || v.severity === severityFilter) &&
    (vaultFilter === 'all' || v.doc_id === vaultFilter)
  );

  const vaults = Array.from(new Set(violations.map(v => v.doc_id)));

  return (
    <Box sx={{ p: 3, bgcolor: darkMode ? '#181818' : '#eaeaea', borderRadius: 2, mb: 2 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography variant="h4" mb={3}>AIFOLIO Elite Compliance & Business Dashboard</Typography>
        <EliteThemeToggle darkMode={darkMode} onToggle={()=>setDarkMode(!darkMode)} />
      </Box>
      <Tabs value={tab} onChange={(e, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab label="Compliance Feed" />
        <Tab label="Reviewer Leaderboard" />
        <Tab label="Security & Performance" />
        <Tab label="Exports" />
        <Tab label="SAFE AI Score" />
        <Tab label="Heartbeat" />
        <Tab label="Advanced Analytics" />
        {/* --- Extension Point: Add future elite analytics tabs here --- */}
      </Tabs>
      {tab === 0 && (
        <Box>
          <Grid container spacing={3}>
            {/* Compliance Feed */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" mb={2}>Compliance Feed</Typography>
                {loading ? <CircularProgress /> : (
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Vault</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Severity</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>SLA</TableCell>
                        <TableCell>Reviewer</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {violations.map((v, i) => (
                        <TableRow key={i}>
                          <TableCell>{v.doc_id}</TableCell>
                          <TableCell>{v.description}</TableCell>
                          <TableCell><Chip label={v.severity} color={v.severity==='critical'?'error':v.severity==='major'?'warning':'info'} /></TableCell>
                          <TableCell><Chip label={v.status} color={statusColors[v.sla_status]||'default'} /></TableCell>
                          <TableCell><Chip label={v.sla_status} color={statusColors[v.sla_status]||'default'} /></TableCell>
                          <TableCell>{maskReviewer(v.assigned_reviewer)}</TableCell>
                          <TableCell>
                            {v.status==='open' && <Button size="small" color="success" onClick={()=>handleRemediate(i)}>Remediate</Button>}
                            {v.status==='resolved' && <Button size="small" color="warning" onClick={()=>handleRollback(i)}>Rollback</Button>}
                            <Button size="small" color="info" onClick={()=>handleExport('pdf', v.doc_id)}>Export PDF</Button>
                            <Button size="small" color="secondary" onClick={()=>handleDrilldown(v)}>Drilldown</Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </Paper>
            </Grid>
            {/* Reviewer Leaderboard */}
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" mb={2}>Reviewer Leaderboard</Typography>
                {loading ? <CircularProgress /> : (
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Accuracy</TableCell>
                        <TableCell>Resolved</TableCell>
                        <TableCell>Badges</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {leaderboard.map((r, i) => (
                        <TableRow key={i}>
                          <TableCell>{r.name}</TableCell>
                          <TableCell>{(r.accuracy*100).toFixed(1)}%</TableCell>
                          <TableCell>{r.resolved}</TableCell>
                          <TableCell>{r.badges.map((b,j)=><Chip key={j} label={b} color="primary" sx={{mr:0.5}} />)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </Paper>
            </Grid>
          </Grid>
        </Box>
      )}
      {tab === 1 && <EliteKPIDashboard />}
      {tab === 2 && <EliteAIAnalyticsPanel />}
      {tab === 3 && <EliteRuleEditor />}
      {tab === 4 && <EliteAlertRoutingPanel />}
      {tab === 6 && (
        <EliteAdvancedAnalyticsPanel />
      )}
      {/* --- Extension Point: Render future analytics panels here --- */}
      {tab === 7 && <EliteGamificationPanel />}
      {tab === 8 && <EliteExportPanel />}
      {tab === 9 && <EliteAuditSimulationPanel />}
      {tab === 10 && <EliteSAFEAIScorePanel />}
      {tab === 11 && <EliteBusinessIntegrationsPanel />}
      {tab === 12 && <EliteSecurityPerformancePanel />}
      {tab === 13 && <EliteComplianceExportsPanel />}
      {tab === 14 && <EliteHeartbeatPanel />}

      <EliteDrilldownModal open={drilldownOpen} onClose={()=>setDrilldownOpen(false)} event={drilldownEvent} />
      <Snackbar open={!!snackbar} autoHideDuration={3000} onClose={()=>setSnackbar('')} message={snackbar} />
    </Box>
  </Box>
);

export default EliteComplianceDashboard;
