import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Grid,
  Divider,
  Chip,
  CircularProgress,
  Button,
} from "@mui/material";

const analyticsEndpoints = [
  {
    label: "Refund Risk",
    path: "/api/analytics/refund_risk",
    method: "POST",
    sample: {
      vault_id: "vault_001",
      sales: [{ id: 1 }],
      refunds: [{ vault_id: "vault_001" }],
    },
  },
  {
    label: "Asset Health",
    path: "/api/analytics/asset_health",
    method: "POST",
    sample: { vault_id: "vault_001", assets: [{ status: "ok", weight: 2 }] },
  },
  {
    label: "Tone/Voice",
    path: "/api/analytics/tone_voice",
    method: "POST",
    sample: { text: "Brand match text", brand_profile: "Brand" },
  },
  {
    label: "Typo/Grammar",
    path: "/api/analytics/typo_grammar",
    method: "POST",
    sample: { text: "This is teh elite recieve test." },
  },
  {
    label: "Anomaly Detection",
    path: "/api/analytics/anomaly_detection",
    method: "POST",
    sample: {
      vault_id: "vault_001",
      sales: [{ timestamp: new Date().toISOString() }],
    },
  },
  {
    label: "Marketplace Trends",
    path: "/api/analytics/marketplace_trends",
    method: "GET",
    sample: null,
  },
  // --- Extension Point: Add future static SAFE AI modules here ---
];

export default function EliteAdvancedAnalyticsPanel() {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);

  const runAnalytics = async (endpoint, method, sample) => {
    setLoading(true);
    try {
      let res, data;
      if (method === "GET") {
        res = await fetch(endpoint);
      } else {
        res = await fetch(endpoint, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(sample),
        });
      }
      data = await res.json();
      setResults((r) => ({ ...r, [endpoint]: data }));
    } catch {
      setResults((r) => ({ ...r, [endpoint]: { error: true } }));
    }
    setLoading(false);
  };

  useEffect(() => {
    analyticsEndpoints.forEach((a) => runAnalytics(a.path, a.method, a.sample));
  }, []);

  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        Elite Advanced Analytics
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Grid container spacing={2}>
        {analyticsEndpoints.map((a) => (
          <Grid item xs={12} md={6} key={a.label}>
            <Paper sx={{ p: 2, mb: 2 }}>
              <Typography variant="subtitle1">{a.label}</Typography>
              <Button
                variant="outlined"
                size="small"
                sx={{ mb: 1 }}
                onClick={() => runAnalytics(a.path, a.method, a.sample)}
              >
                Run
              </Button>
              {loading ? (
                <CircularProgress size={20} />
              ) : (
                <>
                  <pre
                    style={{
                      background: "#f9f9f9",
                      padding: 8,
                      borderRadius: 4,
                      fontSize: 13,
                    }}
                  >
                    {JSON.stringify(results[a.path], null, 2)}
                  </pre>
                  {results[a.path] &&
                    (results[a.path].SAFE_AI_COMPLIANT ||
                      results[a.path].SAFE_AI_COMPLIANT === true) && (
                      <Chip
                        label="SAFE AI"
                        color="success"
                        size="small"
                        sx={{ mt: 1 }}
                      />
                    )}
                </>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
}
