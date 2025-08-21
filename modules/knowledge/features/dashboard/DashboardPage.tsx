import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardHeader } from '../../ui/components/display/Card';
import { Badge, StatusBadge } from '../../ui/components/display/Badge';
import { Button } from '../../ui/components/forms/Button';
import { useMounted } from '../../hooks/useMounted';

interface DashboardStats {
  totalProjects: number;
  activeAgents: number;
  vaultStatus: 'standby' | 'active' | 'maintenance';
  systemHealth: number;
  lastUpdate: string;
}

interface ActivityItem {
  id: string;
  type: 'system' | 'user' | 'vault' | 'agent';
  message: string;
  timestamp: string;
  status: 'success' | 'warning' | 'error' | 'info';
}

export const DashboardPage: React.FC = () => {
  const mounted = useMounted();
  const [stats, setStats] = useState<DashboardStats>({
    totalProjects: 12,
    activeAgents: 0,
    vaultStatus: 'standby',
    systemHealth: 98,
    lastUpdate: new Date().toISOString(),
  });

  const [activities, setActivities] = useState<ActivityItem[]>([
    {
      id: '1',
      type: 'system',
      message: 'AppShell Control Layer initialized successfully',
      timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
      status: 'success',
    },
    {
      id: '2',
      type: 'vault',
      message: 'Vault system in standby mode - awaiting activation',
      timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
      status: 'info',
    },
    {
      id: '3',
      type: 'user',
      message: 'Theme system preferences updated',
      timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
      status: 'success',
    },
    {
      id: '4',
      type: 'system',
      message: 'Layout fusion components loaded',
      timestamp: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
      status: 'success',
    },
  ]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (mounted) {
      console.log('📊 Dashboard: Page loaded');
      console.log('📦 VAULT: Dashboard view - standby mode');
    }
  }, [mounted]);

  const handleRefresh = async () => {
    setLoading(true);
    console.log('🔄 Dashboard: Refreshing data...');

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    setStats(prev => ({
      ...prev,
      systemHealth: Math.floor(Math.random() * 5) + 95,
      lastUpdate: new Date().toISOString(),
    }));

    setLoading(false);
    console.log('✅ Dashboard: Data refreshed');
  };

  const handleVaultAccess = () => {
    console.log('📦 VAULT: Access attempted from dashboard');
    console.log('🔒 VAULT: Access denied - System in standby mode');
  };

  if (!mounted) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} loading />
          ))}
        </div>
      </div>
    );
  }

  const formatTimeAgo = (timestamp: string) => {
    const diff = Date.now() - new Date(timestamp).getTime();
    const minutes = Math.floor(diff / 60000);
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  };

  const getActivityIcon = (type: ActivityItem['type']) => {
    const icons = {
      system: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      user: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
      vault: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
      agent: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
    };
    return icons[type];
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-primary">Dashboard</h1>
          <p className="text-secondary mt-1">AIFOLIO Elite System Control Center</p>
        </div>
        <Button
          onClick={handleRefresh}
          loading={loading}
          icon={
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          }
        >
          Refresh
        </Button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card hover>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-secondary">Total Projects</p>
                <p className="text-2xl font-bold text-primary">{stats.totalProjects}</p>
              </div>
              <div className="p-3 bg-primary-100 dark:bg-primary-900/50 rounded-lg">
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card hover>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-secondary">Active Agents</p>
                <p className="text-2xl font-bold text-primary">{stats.activeAgents}</p>
              </div>
              <div className="p-3 bg-vault-100 dark:bg-vault-900/50 rounded-lg">
                <svg className="w-6 h-6 text-vault-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card hover>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-secondary">Vault Status</p>
                <div className="flex items-center space-x-2 mt-1">
                  <StatusBadge status={stats.vaultStatus === 'standby' ? 'pending' : 'active'} />
                  <span className="text-sm font-medium text-primary capitalize">{stats.vaultStatus}</span>
                </div>
              </div>
              <div className="p-3 bg-yellow-100 dark:bg-yellow-900/50 rounded-lg">
                <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card hover>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-secondary">System Health</p>
                <div className="flex items-center space-x-2 mt-1">
                  <p className="text-2xl font-bold text-primary">{stats.systemHealth}%</p>
                  <Badge variant="success" size="xs">Excellent</Badge>
                </div>
              </div>
              <div className="p-3 bg-green-100 dark:bg-green-900/50 rounded-lg">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Feed */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader
              title="Recent Activity"
              subtitle="System events and user actions"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              }
            />
            <div className="space-y-4 mt-4">
              {activities.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + index * 0.1 }}
                  className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200"
                >
                  <div className={`p-2 rounded-full ${
                    activity.status === 'success' ? 'bg-green-100 dark:bg-green-900/50 text-green-600' :
                    activity.status === 'warning' ? 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-600' :
                    activity.status === 'error' ? 'bg-red-100 dark:bg-red-900/50 text-red-600' :
                    'bg-blue-100 dark:bg-blue-900/50 text-blue-600'
                  }`}>
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-primary">{activity.message}</p>
                    <p className="text-xs text-secondary mt-1">{formatTimeAgo(activity.timestamp)}</p>
                  </div>
                  <Badge variant={activity.type === 'vault' ? 'warning' : 'default'} size="xs">
                    {activity.type}
                  </Badge>
                </motion.div>
              ))}
            </div>
          </Card>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card>
            <CardHeader
              title="Quick Actions"
              subtitle="System controls"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              }
            />
            <div className="space-y-3 mt-4">
              <Button
                fullWidth
                variant="primary"
                onClick={handleVaultAccess}
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                }
              >
                Access Vault
              </Button>
              <Button
                fullWidth
                variant="secondary"
                onClick={() => console.log('🔧 System diagnostics requested')}
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                }
              >
                System Diagnostics
              </Button>
              <Button
                fullWidth
                variant="ghost"
                onClick={() => console.log('⚙️ Settings panel requested')}
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                }
              >
                Preferences
              </Button>
            </div>

            {/* System Info */}
            <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="space-y-2 text-xs text-secondary">
                <div className="flex justify-between">
                  <span>Last Update:</span>
                  <span>{formatTimeAgo(stats.lastUpdate)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Build:</span>
                  <span>Phase 1.4</span>
                </div>
                <div className="flex justify-between">
                  <span>Status:</span>
                  <StatusBadge status="online" />
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};
