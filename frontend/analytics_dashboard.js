import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';
import { format } from 'date-fns';
import { useTheme } from '../theme/ThemeProvider';

const AnalyticsDashboard = () => {
  const { theme } = useTheme();
  const [metrics, setMetrics] = useState({
    request_rate: 0,
    error_rate: 0,
    average_response_time: 0,
    cache_hit_rate: 0,
    memory_usage: 0,
    uptime: 0,
    user_engagement: {},
    loading: true
  });

  const [chartData, setChartData] = useState({
    series: [{
      name: 'Request Rate',
      data: []
    }],
    options: {
      chart: {
        type: 'line',
        height: 350
      },
      xaxis: {
        type: 'datetime',
        labels: {
          datetimeUTC: false
        }
      },
      yaxis: {
        title: {
          text: 'Requests per minute'
        }
      }
    }
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get('/analytics');
        setMetrics(response.data);
        updateChartData(response.data);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      }
    };

    // Initial fetch
    fetchMetrics();

    // Poll for updates
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  const updateChartData = (newMetrics) => {
    const now = new Date();
    const data = chartData.series[0].data;
    
    // Add new data point
    data.push({
      x: now,
      y: newMetrics.request_rate
    });
    
    // Keep only last 30 data points
    if (data.length > 30) {
      data.shift();
    }
    
    setChartData(prev => ({
      ...prev,
      series: [{
        name: 'Request Rate',
        data
      }]
    }));
  };

  const formatMetric = (value, unit = '') => {
    return `${value.toFixed(2)} ${unit}`;
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div style={{
      padding: theme.spacing.xxl,
      backgroundColor: theme.colors.background.surface,
      borderRadius: theme.borderRadius.lg,
      boxShadow: theme.shadows.md
    }}>
      <h2 style={{
        fontSize: theme.typography.h2.fontSize,
        fontWeight: theme.typography.h2.fontWeight,
        marginBottom: theme.spacing.md,
        color: theme.colors.text.primary
      }}>Analytics Dashboard</h2>

      {/* Real-time metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          </div>
        ))}
      </div>

      {/* Request rate chart */}
      <div className="mb-8">
        <h3 className={`text-xl font-semibold mb-4 ${theme.text.primary}`}>Request Rate Over Time</h3>
        <Chart 
          options={chartData.options}
          series={chartData.series}
          type="line"
          height={350}
        />
      </div>

      {/* User engagement */}
      <div>
        <h3 className={`text-xl font-semibold mb-4 ${theme.text.primary}`}>User Engagement</h3>
        <div className="space-y-4">
          {Object.entries(metrics.user_engagement).map(([userId, actions]) => (
            <div key={userId} className={`bg-gray-800 p-4 rounded-lg ${theme.background.surface}`}>
              <h4 className={`text-lg font-semibold mb-2 ${theme.text.secondary}`}>User {userId}</h4>
              <ul className="space-y-2">
                {Object.entries(actions).map(([action, count]) => (
                  <li key={action} className="flex justify-between">
                    <span className={`text-gray-400 ${theme.text.secondary}`}>{action}</span>
                    <span className={`font-medium ${theme.text.primary}`}>{count}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
