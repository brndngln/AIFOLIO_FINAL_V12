// [WINDSURF FIXED ✅]
import React, { useState, useEffect } from "react";
// [WINDSURF FIXED]
import PrivacyStatusBar from "./PrivacyStatusBar"; // [WINDSURF FIXED]
import VaultDropCountdownPanel from "./VaultDropCountdownPanel"; // [WINDSURF FIXED]
import SalesHeatmapPanel from "./SalesHeatmapPanel"; // [WINDSURF FIXED]
import AILogVisualizerPanel from "./AILogVisualizerPanel"; // [WINDSURF FIXED]
import ComplianceRiskScoreWidget from "./ComplianceRiskScoreWidget"; // [WINDSURF FIXED]
import AutomationTriggerPanel from "./AutomationTriggerPanel"; // [WINDSURF FIXED]
import AuditLogSearchPanel from "./AuditLogSearchPanel"; // [WINDSURF FIXED]

// [WINDSURF FIXED ✅]
function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState({
    request_rate: 0,
    error_rate: 0,
    memory_usage: 0,
    cache_hit_rate: 0,
    user_engagement: {
      user1: { clicks: 0, views: 0 },
      user2: { clicks: 0, views: 0 },
    },
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const token: "YOUR_TOKEN_HERE"("token");
        const response = await fetch("/api/analytics/metrics", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) throw new Error("Failed to fetch metrics");
        const data = await response.json();
        setMetrics(data);
      } catch (error) {
        console.error("Error fetching analytics metrics:", error);
      }
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  const formatMetric = (value, unit = "") => {
    return `${value}${unit}`;
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Import creative dashboard panels
  // (Assume imports are added at the top)
  // import VaultDropCountdownPanel from './VaultDropCountdownPanel';
  // import SalesHeatmapPanel from './SalesHeatmapPanel';
  // import AILogVisualizerPanel from './AILogVisualizerPanel';
  // import ComplianceRiskScoreWidget from './ComplianceRiskScoreWidget';
  // import AutomationTriggerPanel from './AutomationTriggerPanel';

  // Import creative dashboard panels
  // (Assume imports are added at the top)
  // import PrivacyStatusBar from './PrivacyStatusBar';
  // import AuditLogSearchPanel from './AuditLogSearchPanel';

  return (
    <div className="space-y-6">
      {/* Accessibility/Compliance: Privacy status always visible */}
      <PrivacyStatusBar />
      <h2
        className="text-2xl font-bold"
        style={{
          color: "var(--text)",
          backgroundColor: "var(--accent)",
          padding: "var(--spacing-md)",
          borderRadius: "var(--border-radius-md)",
          boxShadow: "var(--shadow-sm)",
        }}
        aria-label="Analytics Dashboard Heading"
      >
        Analytics Dashboard
      </h2>

      {/* Creative/Unique Panels */}
      <section aria-label="Vault Drop Countdown">
        <VaultDropCountdownPanel />
      </section>
      <section aria-label="Sales Heatmap">
        <SalesHeatmapPanel />
      </section>
      <section aria-label="AI Log Visualizer">
        <AILogVisualizerPanel />
      </section>
      <section aria-label="Compliance Risk Score">
        <ComplianceRiskScoreWidget />
      </section>
      <section aria-label="Automation Triggers">
        <AutomationTriggerPanel />
      </section>

      {/* Audit Log Search Panel */}
      <section aria-label="Audit Log Search">
        <AuditLogSearchPanel />
      </section>

      {/* Main Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div
          className="theme-card"
          style={{
            animation: "var(--animation-fade-in)",
            borderColor: "var(--secondary)",
            borderWidth: "1px",
            borderStyle: "solid",
          }}
        >
          <h3
            className="text-lg font-semibold"
            style={{
              color: "var(--text)",
              backgroundColor: "var(--accent)",
              padding: "var(--spacing-sm)",
              borderRadius: "var(--border-radius-sm)",
            }}
            aria-label="Request Rate"
          >
            Request Rate
          </h3>
          <p
            className="text-2xl font-bold"
            style={{
              color: "var(--text)",
              marginTop: "var(--spacing-md)",
            }}
          >
            {formatMetric(metrics.request_rate, "req/min")}
          </p>
        </div>

        <div
          className="theme-card"
          style={{
            animation: "var(--animation-fade-in)",
            borderColor: "var(--secondary)",
            borderWidth: "1px",
            borderStyle: "solid",
          }}
        >
          <h3
            className="text-lg font-semibold"
            style={{
              color: "var(--text)",
              backgroundColor: "var(--accent)",
              padding: "var(--spacing-sm)",
              borderRadius: "var(--border-radius-sm)",
            }}
          >
            Error Rate
          </h3>
          <p
            className="text-2xl font-bold"
            style={{
              color:
                metrics.error_rate > 2 ? "var(--secondary)" : "var(--text)",
              marginTop: "var(--spacing-md)",
            }}
          >
            {formatPercentage(metrics.error_rate)}
          </p>
        </div>

        <div
          className="theme-card"
          style={{
            animation: "var(--animation-fade-in)",
            borderColor: "var(--secondary)",
            borderWidth: "1px",
            borderStyle: "solid",
          }}
        >
          <h3
            className="text-lg font-semibold"
            style={{
              color: "var(--text)",
              backgroundColor: "var(--accent)",
              padding: "var(--spacing-sm)",
              borderRadius: "var(--border-radius-sm)",
            }}
          >
            Cache Hit Rate
          </h3>
          <p
            className="text-2xl font-bold"
            style={{
              color:
                metrics.cache_hit_rate > 80 ? "var(--accent)" : "var(--text)",
              marginTop: "var(--spacing-md)",
            }}
          >
            {formatPercentage(metrics.cache_hit_rate)}
          </p>
        </div>

        <div
          className="theme-card"
          style={{
            animation: "var(--animation-fade-in)",
            borderColor: "var(--secondary)",
            borderWidth: "1px",
            borderStyle: "solid",
          }}
        >
          <h3
            className="text-lg font-semibold"
            style={{
              color: "var(--text)",
              backgroundColor: "var(--accent)",
              padding: "var(--spacing-sm)",
              borderRadius: "var(--border-radius-sm)",
            }}
          >
            Memory Usage
          </h3>
          <div className="flex items-center space-x-2 mt-2">
            <span
              className="text-2xl font-bold"
              style={{
                color: "var(--text)",
              }}
            >
              {formatMetric(metrics.memory_usage, "MB")}
            </span>
            <span
              className={`theme-metric ${metrics.memory_usage > 80 ? "warning" : "stable"}`}
            >
              {metrics.memory_usage > 80 ? "Warning" : "Stable"}
            </span>
          </div>
        </div>
      </div>

      <div className="mb-8">
        <h3
          className="text-xl font-semibold mb-4"
          style={{
            color: "var(--text)",
            backgroundColor: "var(--accent)",
            padding: "var(--spacing-sm)",
            borderRadius: "var(--border-radius-sm)",
          }}
        >
          Request Rate Over Time
        </h3>
        <div className="theme-card">
          <div
            className="h-64"
            style={{
              backgroundColor: "var(--card)",
              borderRadius: "var(--border-radius-lg)",
              boxShadow: "var(--shadow-md)",
            }}
          >
            Chart will be here
          </div>
        </div>
      </div>

      <div>
        <h3
          className="text-xl font-semibold mb-4"
          style={{
            color: "var(--text)",
            backgroundColor: "var(--accent)",
            padding: "var(--spacing-sm)",
            borderRadius: "var(--border-radius-sm)",
          }}
        >
          User Engagement
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(metrics.user_engagement).map(([userId, actions]) => (
            <div
              key={userId}
              className="theme-card"
              style={{
                animation: "var(--animation-fade-in)",
                borderColor: "var(--secondary)",
                borderWidth: "1px",
                borderStyle: "solid",
              }}
            >
              <h4
                className="text-lg font-semibold mb-2"
                style={{
                  color: "var(--text)",
                  backgroundColor: "var(--accent)",
                  padding: "var(--spacing-sm)",
                  borderRadius: "var(--border-radius-sm)",
                }}
              >
                User {userId}
              </h4>
              <ul className="space-y-2">
                {Object.entries(actions).map(([action, count]) => (
                  <li key={action} className="flex justify-between">
                    <span
                      style={{
                        color: "var(--text)",
                        fontSize: "var(--font-size-sm)",
                      }}
                    >
                      {action}
                    </span>
                    <span
                      className="font-medium"
                      style={{
                        color: "var(--accent)",
                        fontSize: "var(--font-size-sm)",
                      }}
                    >
                      {count}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// No props for AnalyticsDashboard; PropTypes not required. [WINDSURF FIXED]

export default AnalyticsDashboard; // [WINDSURF FIXED]
