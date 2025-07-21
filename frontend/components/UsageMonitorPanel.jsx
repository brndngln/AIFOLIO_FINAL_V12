import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Alert,
  Button,
  CircularProgress,
  Tooltip,
  IconButton,
  Chip,
  Stack,
  Menu,
  MenuItem,
} from "@mui/material";
import { Line } from "react-chartjs-2";
import RefreshIcon from "@mui/icons-material/Refresh";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DownloadIcon from "@mui/icons-material/Download";

const ADMIN_ROLES = ["OWNER", "AUDITOR"]; // Only these can export
const UsageMonitorPanel = ({ adminId, adminRoles = [] }) => {
  const [usage, setUsage] = useState({});
  const [anomalies, setAnomalies] = useState([]);
  const [autoFreeze, setAutoFreeze] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState({ total: 0, keys: 0 });
  const [anchorEl, setAnchorEl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [downloadName, setDownloadName] = useState("");

  const fetchData = () => {
    setLoading(true);
    Promise.all([
      axios.get("/api/usage/metrics"),
      axios.get("/api/usage/anomalies"),
      axios.get("/config/vault_control_flags.json"),
    ])
      .then(([usageRes, anomalyRes, configRes]) => {
        setUsage(usageRes.data);
        setAnomalies(anomalyRes.data);
        setAutoFreeze(!!configRes.data.auto_freeze_on_spike);
        // Calculate summary
        let total = 0,
          keys = 0;
        Object.values(usageRes.data).forEach((dayObj) => {
          total += Object.values(dayObj).reduce((a, b) => a + b, 0);
          keys++;
        });
        setSummary({ total, keys });
      })
      .catch(() => setError("Failed to load usage or config data."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAutoFreezeToggle = () => {
    axios
      .post("/api/usage/auto-freeze", { enable: !autoFreeze })
      .then(() => setAutoFreeze(!autoFreeze))
      .catch(() => setError("Failed to update auto-freeze setting."));
  };

  // Prepare chart data
  const keys = Object.keys(usage);
  const labels = keys.length ? Object.keys(usage[keys[0]]) : [];
  const chartData = {
    labels,
    datasets: keys.map((k, i) => ({
      label: k,
      data: Object.values(usage[k]),
      borderColor: `hsl(${i * 60},70%,50%)`,
      backgroundColor: `hsla(${i * 60},70%,50%,0.2)`,
      fill: false,
      tension: 0.2,
      pointRadius: 3,
    })),
  };

  const handleExport = (log, format) => {
    axios
      .get(`/api/export/audit?format=${format}&log=${log}`, {
        responseType: "blob",
      })
      .then((res) => {
        const url = window.URL.createObjectURL(new Blob([res.data]));
        setDownloadUrl(url);
        setDownloadName(
          `${log}_audit_${new Date().toISOString().slice(0, 10)}.${format}`,
        );
        setTimeout(() => setDownloadUrl(""), 10000); // Clean up after 10s
      })
      .catch(() => setError("Failed to export audit log."));
  };

  return (
    <Box sx={{ p: 2, bgcolor: "#fff", borderRadius: 2, mb: 2, minHeight: 380 }}>
      <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Secret Usage Monitor
        </Typography>
        <Tooltip title="Refresh">
          <IconButton onClick={fetchData} aria-label="refresh" size="small">
            <RefreshIcon />
          </IconButton>
        </Tooltip>
        {adminRoles.some((r) => ADMIN_ROLES.includes(r)) && (
          <>
            <Tooltip title="Export Audit Log">
              <IconButton
                aria-label="export"
                size="small"
                onClick={(e) => setAnchorEl(e.currentTarget)}
              >
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            <Menu
              anchorEl={anchorEl}
              open={!!anchorEl}
              onClose={() => setAnchorEl(null)}
            >
              {[
                ["rotation", "Secret Rotations"],
                ["anomaly", "Usage Spikes"],
                ["override", "Overrides"],
              ].map(([log, label]) => (
                <MenuItem
                  key={log + "json"}
                  onClick={() => {
                    setAnchorEl(null);
                    handleExport(log, "json");
                  }}
                >
                  {label} (JSON)
                </MenuItem>
              ))}
              {[
                ["rotation", "Secret Rotations"],
                ["anomaly", "Usage Spikes"],
                ["override", "Overrides"],
              ].map(([log, label]) => (
                <MenuItem
                  key={log + "csv"}
                  onClick={() => {
                    setAnchorEl(null);
                    handleExport(log, "csv");
                  }}
                >
                  {label} (CSV)
                </MenuItem>
              ))}
            </Menu>
          </>
        )}
      </Box>
      {loading ? (
        <CircularProgress
          size={32}
          sx={{ display: "block", mx: "auto", my: 4 }}
        />
      ) : (
        <>
          {error && <Alert severity="error">{error}</Alert>}
          <Line
            data={chartData}
            options={{
              plugins: { legend: { position: "bottom" } },
              scales: { y: { beginAtZero: true } },
            }}
          />
          <Stack direction="row" spacing={2} sx={{ mt: 2, mb: 1 }}>
            <Chip
              icon={<CheckCircleIcon color="success" />}
              label={`Tracked Keys: ${summary.keys}`}
            />
            <Chip
              icon={<CheckCircleIcon color="primary" />}
              label={`Total Calls: ${summary.total}`}
            />
            <Chip
              icon={
                autoFreeze ? (
                  <WarningAmberIcon color="error" />
                ) : (
                  <CheckCircleIcon color="success" />
                )
              }
              label={autoFreeze ? "Auto-Freeze ON" : "Auto-Freeze OFF"}
              color={autoFreeze ? "error" : "success"}
            />
          </Stack>
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2">Recent Spike Events:</Typography>
            {anomalies.length === 0 && (
              <Typography variant="body2" color="text.secondary">
                No recent spikes detected.
              </Typography>
            )}
            {anomalies
              .slice(-3)
              .reverse()
              .map((a, i) => (
                <Alert
                  severity="warning"
                  key={i}
                  icon={<WarningAmberIcon fontSize="inherit" />}
                  sx={{ mb: 1 }}
                >
                  <b>{a.timestamp}</b>: <b>{a.key}</b> spiked to{" "}
                  <b>{a.current}</b> (avg {a.avg.toFixed(2)})
                </Alert>
              ))}
          </Box>
          <Button
            variant={autoFreeze ? "contained" : "outlined"}
            color={autoFreeze ? "error" : "primary"}
            onClick={handleAutoFreezeToggle}
            sx={{ mt: 2 }}
            aria-label="toggle auto-freeze"
          >
            {autoFreeze ? "Auto-Freeze ON" : "Enable Auto-Freeze on Next Spike"}
          </Button>
          {downloadUrl && (
            <Box sx={{ mt: 2 }}>
              <a
                href={downloadUrl}
                download={downloadName}
                style={{ textDecoration: "none" }}
              >
                <Button variant="contained" color="success" size="small">
                  Download {downloadName}
                </Button>
              </a>
            </Box>
          )}
        </>
      )}
    </Box>
  );
};
export default UsageMonitorPanel;
