// [WINDSURF FIXED ✅]
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types"; // [WINDSURF FIXED]
import { useTheme } from "../theme/ThemeProvider";
import axios from "axios";
import { format } from "date-fns";

const EthicalDashboard = () => {
  const { theme } = useTheme();
  const [activityLog, setActivityLog] = useState([]);
  const [metrics, setMetrics] = useState({
    totalActions: 0,
    suspiciousPatterns: 0,
    rateLimitHits: 0,
    memoryWarnings: 0,
    lastCheck: null,
  });

  useEffect(() => {
    // Fetch initial data
    fetchData();

    // Update every minute
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const token: "YOUR_TOKEN_HERE"("token");
      // Fetch activity log
      const activityResponse = await axios.get("/api/monitor/activity", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setActivityLog(activityResponse.data);

      // Fetch metrics
      const metricsResponse = await axios.get("/api/monitor/metrics", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMetrics(metricsResponse.data);
    } catch (error) {
      console.error("Error fetching compliance/ethics data:", error);
    }
  };

  const formatTimestamp = (timestamp) => {
    return format(new Date(timestamp), "MMM d, yyyy HH:mm:ss");
  };

  return (
    <div
      className="ethical-dashboard"
      style={{
        backgroundColor: theme.background,
        color: theme.text,
        padding: "2rem",
        borderRadius: "8px",
        boxShadow: theme.shadow,
      }}
    >
      <h2
        style={{
          color: theme.accent,
          borderBottom: `1px solid ${theme.border}`,
          paddingBottom: "1rem",
        }}
      >
        Ethical Compliance Dashboard
      </h2>

      <div
        className="metrics-grid"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "1rem",
          marginTop: "2rem",
        }}
      >
        <MetricCard
          label="Total Actions"
          value={metrics.totalActions}
          color={theme.accent}
        />
        <MetricCard
          label="Suspicious Patterns"
          value={metrics.suspiciousPatterns}
          color={metrics.suspiciousPatterns > 0 ? theme.error : theme.secondary}
        />
        <MetricCard
          label="Rate Limit Hits"
          value={metrics.rateLimitHits}
          color={metrics.rateLimitHits > 0 ? theme.error : theme.secondary}
        />
        <MetricCard
          label="Memory Warnings"
          value={metrics.memoryWarnings}
          color={metrics.memoryWarnings > 0 ? theme.error : theme.secondary}
        />
      </div>

      <div
        className="activity-log"
        style={{
          marginTop: "2rem",
          backgroundColor: theme.secondary,
          padding: "1rem",
          borderRadius: "4px",
        }}
      >
        <h3
          style={{
            color: theme.accent,
            borderBottom: `1px solid ${theme.border}`,
            paddingBottom: "0.5rem",
          }}
        >
          Recent Activity
        </h3>
        <div
          className="log-items"
          style={{
            maxHeight: "400px",
            overflowY: "auto",
            marginTop: "1rem",
          }}
        >
          {activityLog.map((activity) => (
            <div
              key={activity.id}
              className="log-item"
              style={{
                padding: "0.5rem",
                borderBottom: `1px solid ${theme.border}`,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <div>
                <span
                  style={{
                    color: theme.accent,
                    fontWeight: "bold",
                  }}
                >
                  {activity.action}
                </span>
                <span
                  style={{
                    color: theme.text,
                    marginLeft: "0.5rem",
                  }}
                >
                  at {formatTimestamp(activity.timestamp)}
                </span>
              </div>
              <div
                style={{
                  color: activity.metadata.error
                    ? theme.error
                    : theme.secondary,
                }}
              >
                {activity.metadata.error ? "⚠️" : "✅"}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, color }) => {
  const theme = useTheme();
  return (
    <div
      className="metric-card"
      style={{
        padding: "1rem",
        borderRadius: "4px",
        backgroundColor: color,
        color: theme.text,
        textAlign: "center",
      }}
    >
      <h3
        style={{
          color: theme.text,
          marginBottom: "0.5rem",
        }}
      >
        {label}
      </h3>
      <div
        style={{
          fontSize: "1.5rem",
          fontWeight: "bold",
          color: theme.text,
        }}
      >
        {value}
      </div>
    </div>
  );
};

// No props for EthicalDashboard; PropTypes not required. [WINDSURF FIXED]

export default EthicalDashboard; // [WINDSURF FIXED]
