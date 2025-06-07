import React, { useState, useEffect } from 'react';
import { useTheme } from '../theme/ThemeProvider';
import axios from 'axios';
import { format } from 'date-fns';

const SecurityDashboard = () => {
    const { theme } = useTheme();
    const [alerts, setAlerts] = useState([]);
    const [vulnerabilities, setVulnerabilities] = useState([]);
    const [compliance, setCompliance] = useState({
        gdpr: 0,
        ccpa: 0,
        hipaa: 0,
        lastScan: null
    });

    useEffect(() => {
        const fetchSecurityData = async () => {
            try {
                const [alertsRes, vulnsRes, complianceRes] = await Promise.all([
                    axios.get('/api/monitor/security/alerts'),
                    axios.get('/api/monitor/security/vulnerabilities'),
                    axios.get('/api/monitor/security/compliance')
                ]);
                
                setAlerts(alertsRes.data);
                setVulnerabilities(vulnsRes.data);
                setCompliance(complianceRes.data);
            } catch (error) {
                console.error('Error fetching security data:', error);
            }
        };

        // Initial fetch
        fetchSecurityData();
        
        // Update every minute
        const interval = setInterval(fetchSecurityData, 60000);
        return () => clearInterval(interval);
    }, []);

    const formatTimestamp = (timestamp) => {
        return format(new Date(timestamp), 'MMM d, yyyy HH:mm:ss');
    };

    return (
        <div className="security-dashboard" style={{
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
                Security Monitoring
            </h2>

            <div className="security-grid" style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <AlertsCard alerts={alerts} theme={theme} />
                <VulnerabilitiesCard vulnerabilities={vulnerabilities} theme={theme} />
                <ComplianceCard compliance={compliance} theme={theme} />
            </div>
        </div>
    );
};

const AlertsCard = ({ alerts, theme }) => (
    <div className="security-card" style={{
        padding: '1rem',
        borderRadius: '4px',
        backgroundColor: theme.secondary,
        color: theme.text,
        marginTop: '1rem'
    }}>
        <h3 style={{
            color: theme.accent,
            borderBottom: `1px solid ${theme.border}`,
            paddingBottom: '0.5rem'
        }}>Security Alerts</h3>
        <div className="alerts-list" style={{
            maxHeight: '300px',
            overflowY: 'auto',
            marginTop: '1rem'
        }}>
            {alerts.map((alert, index) => (
                <div key={index} className="alert-item" style={{
                    padding: '0.5rem',
                    borderBottom: `1px solid ${theme.border}`,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}>
                    <div>
                        <span style={{
                            color: alert.severity === 'high' ? theme.error : 
                                   alert.severity === 'medium' ? theme.secondary : theme.text,
                            fontWeight: 'bold'
                        }}>{alert.title}</span>
                        <span style={{
                            color: theme.secondary,
                            marginLeft: '0.5rem'
                        }}>at {formatTimestamp(alert.timestamp)}</span>
                    </div>
                    <div style={{
                        color: alert.status === 'resolved' ? theme.accent : theme.error
                    }}>{alert.status.toUpperCase()}</div>
                </div>
            ))}
        </div>
    </div>
);

const VulnerabilitiesCard = ({ vulnerabilities, theme }) => (
    <div className="security-card" style={{
        padding: '1rem',
        borderRadius: '4px',
        backgroundColor: theme.secondary,
        color: theme.text,
        marginTop: '1rem'
    }}>
        <h3 style={{
            color: theme.accent,
            borderBottom: `1px solid ${theme.border}`,
            paddingBottom: '0.5rem'
        }}>Vulnerabilities</h3>
        <div className="vulnerabilities-grid" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '1rem',
            marginTop: '1rem'
        }}>
            {vulnerabilities.map((vuln, index) => (
                <div key={index} className="vulnerability-item" style={{
                    padding: '0.5rem',
                    borderRadius: '4px',
                    backgroundColor: vuln.severity === 'critical' ? theme.error :
                                    vuln.severity === 'high' ? theme.secondary : theme.border,
                    color: theme.text,
                    textAlign: 'center'
                }}>
                    <div style={{
                        color: theme.accent,
                        fontWeight: 'bold'
                    }}>{vuln.title}</div>
                    <div style={{
                        color: theme.secondary,
                        fontSize: '0.8rem'
                    }}>{vuln.severity.toUpperCase()}</div>
                </div>
            ))}
        </div>
    </div>
);

const ComplianceCard = ({ compliance, theme }) => (
    <div className="security-card" style={{
        padding: '1rem',
        borderRadius: '4px',
        backgroundColor: theme.secondary,
        color: theme.text,
        marginTop: '1rem'
    }}>
        <h3 style={{
            color: theme.accent,
            borderBottom: `1px solid ${theme.border}`,
            paddingBottom: '0.5rem'
        }}>Compliance Status</h3>
        <div className="compliance-grid" style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '1rem',
            marginTop: '1rem'
        }}>
            <ComplianceItem
                label="GDPR"
                value={`${compliance.gdpr}%`}
                status={compliance.gdpr >= 90 ? 'good' : compliance.gdpr >= 70 ? 'warning' : 'bad'}
                theme={theme}
            />
            <ComplianceItem
                label="CCPA"
                value={`${compliance.ccpa}%`}
                status={compliance.ccpa >= 90 ? 'good' : compliance.ccpa >= 70 ? 'warning' : 'bad'}
                theme={theme}
            />
            <ComplianceItem
                label="HIPAA"
                value={`${compliance.hipaa}%`}
                status={compliance.hipaa >= 90 ? 'good' : compliance.hipaa >= 70 ? 'warning' : 'bad'}
                theme={theme}
            />
        </div>
        <div className="last-scan" style={{
            marginTop: '1rem',
            color: theme.secondary,
            textAlign: 'right'
        }}>
            Last Scan: {compliance.lastScan ? formatTimestamp(compliance.lastScan) : 'Never'}
        </div>
    </div>
);

const ComplianceItem = ({ label, value, status, theme }) => (
    <div className="compliance-item" style={{
        padding: '0.5rem',
        borderRadius: '4px',
        backgroundColor: status === 'good' ? theme.accent :
                        status === 'warning' ? theme.secondary : theme.error,
        color: theme.text,
        textAlign: 'center'
    }}>
        <div style={{
            color: theme.text,
            fontWeight: 'bold'
        }}>{label}</div>
        <div style={{
            fontSize: '1.2rem',
            fontWeight: 'bold'
        }}>{value}</div>
    </div>
);

export default SecurityDashboard;
