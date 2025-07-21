import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Chip,
  CircularProgress,
  Tooltip,
  Grid,
  Divider,
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import BugReportIcon from "@mui/icons-material/BugReport";
import GroupWorkIcon from "@mui/icons-material/GroupWork";

const API_URL = "/api/events/ai_insights";

export default function EliteAIAnalyticsPanel() {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInsights();
    const interval = setInterval(fetchInsights, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setInsights(data);
    } catch (e) {
      setInsights(null);
    }
    setLoading(false);
  };

  if (loading) return <CircularProgress />;
  if (!insights)
    return <Typography color="error">No insights available.</Typography>;

  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: "bold" }}>
        <TrendingUpIcon sx={{ verticalAlign: "bottom", mr: 1 }} /> AI Analytics
        Insights
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <GroupWorkIcon sx={{ mr: 1 }} />
              Clusters
            </Typography>
            {insights.clusters && insights.clusters.length > 0 ? (
              insights.clusters.map((c, idx) => (
                <Chip key={idx} label={`Cluster ${c}`} sx={{ mr: 1, mb: 1 }} />
              ))
            ) : (
              <Typography variant="body2">No clustering data.</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <BugReportIcon sx={{ mr: 1 }} />
              Anomalies
            </Typography>
            {insights.anomalies && insights.anomalies.length > 0 ? (
              insights.anomalies.map((a, idx) => (
                <Chip
                  key={idx}
                  label={`Event #${a}`}
                  color="error"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))
            ) : (
              <Typography variant="body2">No anomalies detected.</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <TrendingUpIcon sx={{ mr: 1 }} />
              Trends
            </Typography>
            {insights.trends ? (
              Object.entries(insights.trends).map(([k, v]) => (
                <Tooltip key={k} title={k}>
                  <Chip
                    label={`${k}: ${v}`}
                    color={
                      v === "rising"
                        ? "success"
                        : v === "falling"
                          ? "error"
                          : "default"
                    }
                    sx={{ mr: 1, mb: 1 }}
                  />
                </Tooltip>
              ))
            ) : (
              <Typography variant="body2">No trend data.</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
      <Divider sx={{ my: 2 }} />
      <Typography variant="caption" color="text.secondary">
        Last updated: {insights.timestamp || "n/a"}
      </Typography>
    </Box>
  );
}
