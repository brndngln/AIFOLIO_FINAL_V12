import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Grid,
  Paper,
  Chip,
  CircularProgress,
  Tooltip,
  Divider,
  Button,
  Switch,
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AssessmentIcon from "@mui/icons-material/Assessment";
import ScoreIcon from "@mui/icons-material/Score";
import LeaderboardIcon from "@mui/icons-material/Leaderboard";
import { Line, Bar, Heatmap } from "react-chartjs-2";

const API_URL = "/api/kpi/elite";

export default function EliteKPIDashboard() {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    fetchKpis();
    const interval = setInterval(fetchKpis, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchKpis = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setKpis(data);
    } catch (e) {
      setKpis(null);
    }
    setLoading(false);
  };

  if (loading) return <CircularProgress />;
  if (!kpis)
    return <Typography color="error">No KPI data available.</Typography>;

  return (
    <Box
      sx={{
        bgcolor: darkMode ? "#111" : "#fff",
        color: darkMode ? "#eee" : "#222",
        borderRadius: 2,
        p: 3,
      }}
    >
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold" }}>
          <AssessmentIcon sx={{ verticalAlign: "bottom", mr: 1 }} /> Elite KPI
          Dashboard
        </Typography>
        <Box>
          <Tooltip title="Toggle Dark/Light Mode">
            <Switch
              checked={darkMode}
              onChange={(e) => setDarkMode(e.target.checked)}
            />
          </Tooltip>
        </Box>
      </Box>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <ScoreIcon sx={{ mr: 1 }} />
              Compliance Score
            </Typography>
            <Chip
              label={`Score: ${kpis.compliance_score}`}
              color={
                kpis.compliance_score > 90
                  ? "success"
                  : kpis.compliance_score > 75
                    ? "warning"
                    : "error"
              }
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <LeaderboardIcon sx={{ mr: 1 }} />
              Reviewer Response Time
            </Typography>
            <Chip
              label={`Median: ${kpis.reviewer_response_time} min`}
              color="info"
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <TrendingUpIcon sx={{ mr: 1 }} />
              Revenue Trend
            </Typography>
            <Chip
              label={kpis.revenue_trend}
              color={
                kpis.revenue_trend === "rising"
                  ? "success"
                  : kpis.revenue_trend === "falling"
                    ? "error"
                    : "warning"
              }
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <TrendingUpIcon sx={{ mr: 1 }} />
              Refund Risk
            </Typography>
            <Chip
              label={kpis.refund_risk}
              color={
                kpis.refund_risk === "low"
                  ? "success"
                  : kpis.refund_risk === "high"
                    ? "error"
                    : "warning"
              }
            />
          </Paper>
        </Grid>
      </Grid>
      <Divider sx={{ my: 2 }} />
      {/* Animated Trend Chart */}
      <Typography variant="subtitle2" sx={{ mt: 2 }}>
        Revenue, Churn, and Compliance KPIs Over Time
      </Typography>
      <Box sx={{ height: 240 }}>
        {/* Example: <Line data={kpis.kpi_trends} options={{responsive:true}} /> */}
        <Typography variant="body2" color="text.secondary">
          (Trend chart coming soon)
        </Typography>
      </Box>
      <Divider sx={{ my: 2 }} />
      <Button variant="contained" color="primary" sx={{ mt: 2 }}>
        Export All KPIs (CSV)
      </Button>
    </Box>
  );
}
