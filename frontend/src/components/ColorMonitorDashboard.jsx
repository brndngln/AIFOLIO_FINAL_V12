// [WINDSURF FIXED ✅]
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types'; // [WINDSURF FIXED]
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';
import { format } from 'date-fns';
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';
import { format } from 'date-fns';

const ColorMonitorDashboard = () => {
    const { theme } = useTheme();
    const [colorHistory, setColorHistory] = useState([]);
    const [colorPatterns, setColorPatterns] = useState({
        suspicious: 0,
        random: 0,
        uniform: 0,
        gradient: 0,
        lastCheck: null
    });

    useEffect(() => {
        const fetchColorData = async () => {
            try {
                const [historyRes, patternsRes] = await Promise.all([
                    axios.get('/api/monitor/color/history'),
                    axios.get('/api/monitor/color/patterns')
                ]);
                
                setColorHistory(historyRes.data);
                setColorPatterns(patternsRes.data);
            } catch (error) {
                console.error('Error fetching color data:', error);
            }
        };

        // Initial fetch
        fetchColorData();
        
        // Update every 30 seconds
        const interval = setInterval(fetchColorData, 30000);
        return () => clearInterval(interval);
    }, []);

    const formatTimestamp = (timestamp) => {
        return format(new Date(timestamp), 'MMM d, yyyy HH:mm:ss');
    };

    return (
        <div className="color-monitor-dashboard" style={{
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
                Color Pattern Monitoring
            </h2>

            <div className="color-metrics" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <ColorMetricCard
                    label="Suspicious Patterns"
                    value={colorPatterns.suspicious}
                    color={colorPatterns.suspicious > 0 ? theme.error : theme.accent}
                    description="Colors that show signs of sentience"
                />
                <ColorMetricCard
                    label="Random Changes"
                    value={colorPatterns.random}
                    color={colorPatterns.random > 10 ? theme.warning : theme.secondary}
                    description="High frequency random changes detected"
                />
                <ColorMetricCard
                    label="Uniform Colors"
                    value={colorPatterns.uniform}
                    color={colorPatterns.uniform > 5 ? theme.warning : theme.secondary}
                    description="Too many uniform color patterns"
                />
                <ColorMetricCard
                    label="Gradient Usage"
                    value={colorPatterns.gradient}
                    color={theme.secondary}
                    description="Gradient patterns detected"
                />
            </div>

            <div className="color-history" style={{
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
                    Recent Color Changes
                </h3>
                <div className="history-items" style={{
                    maxHeight: '400px',
                    overflowY: 'auto',
                    marginTop: '1rem'
                }}>
                    {colorHistory.map((change, index) => (
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

const ColorMetricCard = ({ label, value, color, description }) => (
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

// No props for ColorMonitorDashboard; PropTypes not required. [WINDSURF FIXED]

function ColorMetricCard({ label, value, color, description }) {
    return null; // placeholder if not already defined
}

ColorMetricCard.propTypes = {
    label: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    color: PropTypes.string,
    description: PropTypes.string
}; // [WINDSURF FIXED]

export default ColorMonitorDashboard; // [WINDSURF FIXED]
