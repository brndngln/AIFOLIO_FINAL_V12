<<<<<<< HEAD
import React, { useState, useEffect } from 'react';
=======
// [WINDSURF FIXED ✅]
// [WINDSURF FIXED ✅]
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types'; // [WINDSURF FIXED]
>>>>>>> omni_repair_backup_20250704_1335
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';
import { format } from 'date-fns';

const PerformanceDashboard = () => {
    const { theme } = useTheme();
    const [metrics, setMetrics] = useState({
<<<<<<< HEAD
        memory: {
            current: 0,
            max: 0,
            growthRate: 0
        },
        cpu: {
            usage: 0,
            load: 0
        },
        network: {
            requests: 0,
            latency: 0,
            errors: 0
        },
=======
        memory: { current: 0, max: 0 },
        cpu: { usage: 0, load: 0 },
        network: { requests: 0, latency: 0, errors: 0 },
>>>>>>> omni_repair_backup_20250704_1335
        lastUpdate: null
    });

    useEffect(() => {
        const updateMetrics = async () => {
            try {
                const response = await axios.get('/api/monitor/performance');
                setMetrics(response.data);
            } catch (error) {
                console.error('Error fetching performance metrics:', error);
            }
        };

        // Initial update
        updateMetrics();
        
        // Update every 10 seconds
        const interval = setInterval(updateMetrics, 10000);
        return () => clearInterval(interval);
    }, []);

    const formatTimestamp = (timestamp) => {
        return format(new Date(timestamp), 'MMM d, yyyy HH:mm:ss');
    };

    return (
        <div className="performance-dashboard" style={{
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
                Performance Metrics
            </h2>

            <div className="metrics-grid" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <MetricCard
                    label="Memory Usage"
                    value={`${(metrics.memory.current / 1024 / 1024).toFixed(2)} MB`}
                    color={theme.accent}
                    subvalue={`Max: ${(metrics.memory.max / 1024 / 1024).toFixed(2)} MB`}
                />
                <MetricCard
                    label="CPU Usage"
                    value={`${metrics.cpu.usage}%`}
                    color={metrics.cpu.usage > 80 ? theme.error : theme.accent}
                    subvalue={`Load: ${metrics.cpu.load}`}
                />
                <MetricCard
                    label="Network Requests"
                    value={metrics.network.requests}
                    color={metrics.network.errors > 0 ? theme.error : theme.accent}
                    subvalue={`Errors: ${metrics.network.errors}`}
                />
                <MetricCard
                    label="Latency"
                    value={`${metrics.network.latency}ms`}
                    color={metrics.network.latency > 100 ? theme.error : theme.accent}
                />
            </div>

            <div className="last-update" style={{
                marginTop: '2rem',
                color: theme.secondary,
                textAlign: 'right'
            }}>
                Last Updated: {metrics.lastUpdate ? formatTimestamp(metrics.lastUpdate) : 'Never'}
            </div>
        </div>
    );
};

<<<<<<< HEAD
const MetricCard = ({ label, value, color, subvalue }) => (
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
        {subvalue && (
            <div style={{
                color: theme.secondary,
                marginTop: '0.5rem'
            }}>{subvalue}</div>
        )}
    </div>
);

export default PerformanceDashboard;
=======
const MetricCard = ({ label, value, color, subvalue }) => {
    const { theme } = useTheme();
    return (
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
            {subvalue && (
                <div style={{
                    color: theme.secondary,
                    marginTop: '0.5rem'
                }}>{subvalue}</div>
            )}
        </div>
    );
};

MetricCard.propTypes = {
    label: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    color: PropTypes.string,
    subvalue: PropTypes.string
}; // [WINDSURF FIXED]

// No props for PerformanceDashboard; PropTypes not required. [WINDSURF FIXED]

export default PerformanceDashboard; // [WINDSURF FIXED]
>>>>>>> omni_repair_backup_20250704_1335
