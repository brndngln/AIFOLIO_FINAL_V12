import React, { useState, useEffect } from 'react';
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';
import { format } from 'date-fns';

const ThemeMonitorDashboard = () => {
    const { theme } = useTheme();
    const [themeMetrics, setThemeMetrics] = useState({
        consistency: 100,
        contrast: 100,
        accessibility: 100,
        changes: 0,
        presets: 0,
        lastChange: null
    });
    const [themeHistory, setThemeHistory] = useState([]);

    useEffect(() => {
        const fetchThemeData = async () => {
            try {
                const [metricsRes, historyRes] = await Promise.all([
                    axios.get('/api/monitor/theme/metrics'),
                    axios.get('/api/monitor/theme/history')
                ]);
                
                setThemeMetrics(metricsRes.data);
                setThemeHistory(historyRes.data);
            } catch (error) {
                console.error('Error fetching theme data:', error);
            }
        };

        // Initial fetch
        fetchThemeData();
        
        // Update every 30 seconds
        const interval = setInterval(fetchThemeData, 30000);
        return () => clearInterval(interval);
    }, []);

    const formatTimestamp = (timestamp) => {
        return format(new Date(timestamp), 'MMM d, yyyy HH:mm:ss');
    };

    return (
        <div className="theme-monitor-dashboard" style={{
            backgroundColor: theme.background,
            color: theme.text,
            padding: '2rem',
            borderRadius: '8px',
            boxShadow: theme.shadow
        }}>
            <h2 style={{
                color: theme.accent,
                borderBottom: `1px solid ${theme.border}`,
                paddingBottom: '1rem'
            }}>
                Theme System Monitoring
            </h2>

            <div className="theme-metrics" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <ThemeMetricCard
                    label="Theme Consistency"
                    value={`${themeMetrics.consistency}%`}
                    color={themeMetrics.consistency < 80 ? theme.error : 
                           themeMetrics.consistency < 90 ? theme.warning : theme.accent}
                    description="Measures theme color consistency"
                />
                <ThemeMetricCard
                    label="Contrast Ratio"
                    value={`${themeMetrics.contrast}%`}
                    color={themeMetrics.contrast < 70 ? theme.error : 
                           themeMetrics.contrast < 80 ? theme.warning : theme.accent}
                    description="Measures text/background contrast"
                />
                <ThemeMetricCard
                    label="Accessibility"
                    value={`${themeMetrics.accessibility}%`}
                    color={themeMetrics.accessibility < 70 ? theme.error : 
                           themeMetrics.accessibility < 80 ? theme.warning : theme.accent}
                    description="Measures WCAG compliance"
                />
                <ThemeMetricCard
                    label="Recent Changes"
                    value={themeMetrics.changes}
                    color={themeMetrics.changes > 10 ? theme.warning : theme.secondary}
                    description="Number of theme changes"
                />
                <ThemeMetricCard
                    label="Presets Used"
                    value={themeMetrics.presets}
                    color={themeMetrics.presets > 5 ? theme.warning : theme.secondary}
                    description="Number of preset applications"
                />
            </div>

            <div className="theme-history" style={{
                marginTop: '2rem',
                backgroundColor: theme.secondary,
                padding: '1rem',
                borderRadius: '4px'
            }}>
                <h3 style={{
                    color: theme.accent,
                    borderBottom: `1px solid ${theme.border}`,
                    paddingBottom: '0.5rem'
                }}>
                    Recent Theme Changes
                </h3>
                <div className="history-items" style={{
                    maxHeight: '400px',
                    overflowY: 'auto',
                    marginTop: '1rem'
                }}>
                    {themeHistory.map((change, index) => (
                        <div key={index} className="history-item" style={{
                            padding: '0.5rem',
                            borderBottom: `1px solid ${theme.border}`,
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}>
                            <div>
                                <span style={{
                                    color: theme.accent,
                                    fontWeight: 'bold'
                                }}>Component: {change.component}</span>
                                <span style={{
                                    color: theme.text,
                                    marginLeft: '0.5rem'
                                }}>State: {change.state}</span>
                                <div style={{
                                    backgroundColor: change.color,
                                    width: '20px',
                                    height: '20px',
                                    borderRadius: '4px',
                                    display: 'inline-block',
                                    marginLeft: '0.5rem'
                                }} />
                            </div>
                            <div style={{
                                color: change.metadata.error ? theme.error : theme.secondary
                            }}>
                                {formatTimestamp(change.timestamp)}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

const ThemeMetricCard = ({ label, value, color, description }) => (
    <div className="metric-card" style={{
        padding: '1rem',
        borderRadius: '4px',
        backgroundColor: color,
        color: theme.text,
        textAlign: 'center'
    }}>
        <h3 style={{
            color: theme.text,
            marginBottom: '0.5rem'
        }}>{label}</h3>
        <div style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: theme.text
        }}>{value}</div>
        <div style={{
            color: theme.secondary,
            marginTop: '0.5rem',
            fontSize: '0.8rem'
        }}>{description}</div>
    </div>
);

export default ThemeMonitorDashboard;
