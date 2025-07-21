import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardHeader } from '../../ui/components/display/Card';
import { Button } from '../../ui/components/forms/Button';
import { Input } from '../../ui/components/forms/Input';
import { Select, SelectOption } from '../../ui/components/forms/Select';
import { Badge } from '../../ui/components/display/Badge';
import { Modal } from '../../ui/components/interactive/Modal';
import { useDarkMode } from '../../hooks/useDarkMode';
import { useMounted } from '../../hooks/useMounted';

interface SettingsData {
  profile: {
    name: string;
    email: string;
    role: string;
  };
  preferences: {
    theme: 'light' | 'dark' | 'system';
    language: string;
    notifications: boolean;
    autoSave: boolean;
  };
  system: {
    vaultAccess: boolean;
    agentPermissions: string;
    debugMode: boolean;
  };
}

export const SettingsPage: React.FC = () => {
  const mounted = useMounted();
  const { theme, toggleTheme } = useDarkMode();
  const [activeTab, setActiveTab] = useState<'profile' | 'preferences' | 'system'>('profile');
  const [showResetModal, setShowResetModal] = useState(false);
  const [loading, setLoading] = useState(false);

  const [settings, setSettings] = useState<SettingsData>({
    profile: {
      name: 'AIFOLIO User',
      email: 'user@aifolio.elite',
      role: 'Administrator',
    },
    preferences: {
      theme: theme as 'light' | 'dark',
      language: 'en',
      notifications: true,
      autoSave: true,
    },
    system: {
      vaultAccess: false,
      agentPermissions: 'restricted',
      debugMode: false,
    },
  });

  const languageOptions: SelectOption[] = [
    { value: 'en', label: 'English' },
    { value: 'es', label: 'Español' },
    { value: 'fr', label: 'Français' },
    { value: 'de', label: 'Deutsch' },
    { value: 'ja', label: '日本語' },
  ];

  const agentPermissionOptions: SelectOption[] = [
    { value: 'restricted', label: 'Restricted Access' },
    { value: 'standard', label: 'Standard Access' },
    { value: 'elevated', label: 'Elevated Access', disabled: true },
    { value: 'admin', label: 'Administrator', disabled: true },
  ];

  const handleSave = async () => {
    setLoading(true);
    console.log('⚙️ Settings: Saving configuration...');
    console.log('📦 VAULT: Settings update - access level maintained');

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    console.log('✅ Settings: Configuration saved successfully');
    setLoading(false);
  };

  const handleReset = async () => {
    setLoading(true);
    console.log('🔄 Settings: Resetting to defaults...');

    // Reset to defaults
    setSettings({
      profile: {
        name: 'AIFOLIO User',
        email: 'user@aifolio.elite',
        role: 'Administrator',
      },
      preferences: {
        theme: 'light',
        language: 'en',
        notifications: true,
        autoSave: true,
      },
      system: {
        vaultAccess: false,
        agentPermissions: 'restricted',
        debugMode: false,
      },
    });

    await new Promise(resolve => setTimeout(resolve, 500));
    setLoading(false);
    setShowResetModal(false);
    console.log('✅ Settings: Reset completed');
  };

  if (!mounted) {
    return (
      <div className="space-y-6">
        <Card loading />
        <Card loading />
      </div>
    );
  }

  const tabs = [
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'preferences', label: 'Preferences', icon: '⚙️' },
    { id: 'system', label: 'System', icon: '🔧' },
  ] as const;

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-primary">Settings</h1>
          <p className="text-secondary mt-1">Configure your AIFOLIO system preferences</p>
        </div>
        <div className="flex space-x-3">
          <Button
            variant="ghost"
            onClick={() => setShowResetModal(true)}
            icon={
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            }
          >
            Reset
          </Button>
          <Button
            onClick={handleSave}
            loading={loading}
            icon={
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            }
          >
            Save Changes
          </Button>
        </div>
      </motion.div>

      {/* Tab Navigation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Card padding="none">
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex-1 px-6 py-4 text-sm font-medium transition-colors duration-200
                  ${activeTab === tab.id
                    ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-600 dark:border-primary-400 bg-primary-50 dark:bg-primary-900/20'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
      >
        {activeTab === 'profile' && (
          <Card>
            <CardHeader
              title="Profile Information"
              subtitle="Manage your account details"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              }
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <Input
                label="Full Name"
                value={settings.profile.name}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  profile: { ...prev.profile, name: e.target.value }
                }))}
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                }
              />
              <Input
                label="Email Address"
                type="email"
                value={settings.profile.email}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  profile: { ...prev.profile, email: e.target.value }
                }))}
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                }
              />
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Role
                </label>
                <div className="flex items-center space-x-2">
                  <Badge variant="primary" size="md">
                    {settings.profile.role}
                  </Badge>
                  <span className="text-sm text-secondary">
                    Contact system administrator to change role
                  </span>
                </div>
              </div>
            </div>
          </Card>
        )}

        {activeTab === 'preferences' && (
          <Card>
            <CardHeader
              title="User Preferences"
              subtitle="Customize your experience"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                </svg>
              }
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Theme
                </label>
                <div className="flex items-center space-x-3">
                  <Button
                    variant={theme === 'light' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => theme !== 'light' && toggleTheme()}
                    icon={
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    }
                  >
                    Light
                  </Button>
                  <Button
                    variant={theme === 'dark' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => theme !== 'dark' && toggleTheme()}
                    icon={
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                      </svg>
                    }
                  >
                    Dark
                  </Button>
                </div>
              </div>

              <Select
                label="Language"
                options={languageOptions}
                value={settings.preferences.language}
                onChange={(value) => setSettings(prev => ({
                  ...prev,
                  preferences: { ...prev.preferences, language: value as string }
                }))}
              />

              <div className="md:col-span-2 space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-primary">Notifications</h4>
                    <p className="text-xs text-secondary">Receive system alerts and updates</p>
                  </div>
                  <button
                    onClick={() => setSettings(prev => ({
                      ...prev,
                      preferences: { ...prev.preferences, notifications: !prev.preferences.notifications }
                    }))}
                    className={`
                      relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200
                      ${settings.preferences.notifications ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'}
                    `}
                  >
                    <span
                      className={`
                        inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200
                        ${settings.preferences.notifications ? 'translate-x-6' : 'translate-x-1'}
                      `}
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-primary">Auto Save</h4>
                    <p className="text-xs text-secondary">Automatically save changes</p>
                  </div>
                  <button
                    onClick={() => setSettings(prev => ({
                      ...prev,
                      preferences: { ...prev.preferences, autoSave: !prev.preferences.autoSave }
                    }))}
                    className={`
                      relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200
                      ${settings.preferences.autoSave ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'}
                    `}
                  >
                    <span
                      className={`
                        inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200
                        ${settings.preferences.autoSave ? 'translate-x-6' : 'translate-x-1'}
                      `}
                    />
                  </button>
                </div>
              </div>
            </div>
          </Card>
        )}

        {activeTab === 'system' && (
          <Card>
            <CardHeader
              title="System Configuration"
              subtitle="Advanced system settings"
              icon={
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              }
            />
            <div className="space-y-6 mt-6">
              <Select
                label="Agent Permissions"
                options={agentPermissionOptions}
                value={settings.system.agentPermissions}
                onChange={(value) => setSettings(prev => ({
                  ...prev,
                  system: { ...prev.system, agentPermissions: value as string }
                }))}
                helperText="Higher permission levels require administrator approval"
              />

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-primary">Vault Access</h4>
                    <p className="text-xs text-secondary">Enable vault system integration</p>
                    <Badge variant="warning" size="xs" className="mt-1">Requires Activation</Badge>
                  </div>
                  <button
                    disabled
                    className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 dark:bg-gray-700 opacity-50 cursor-not-allowed"
                  >
                    <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-primary">Debug Mode</h4>
                    <p className="text-xs text-secondary">Enable detailed system logging</p>
                  </div>
                  <button
                    onClick={() => {
                      setSettings(prev => ({
                        ...prev,
                        system: { ...prev.system, debugMode: !prev.system.debugMode }
                      }));
                      console.log('🐛 Debug mode:', !settings.system.debugMode ? 'enabled' : 'disabled');
                    }}
                    className={`
                      relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200
                      ${settings.system.debugMode ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'}
                    `}
                  >
                    <span
                      className={`
                        inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200
                        ${settings.system.debugMode ? 'translate-x-6' : 'translate-x-1'}
                      `}
                    />
                  </button>
                </div>
              </div>

              {/* System Info */}
              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                <h4 className="text-sm font-medium text-primary mb-3">System Information</h4>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-secondary">Version:</span>
                    <span className="ml-2 font-mono">Phase 1.4</span>
                  </div>
                  <div>
                    <span className="text-secondary">Build:</span>
                    <span className="ml-2 font-mono">2025.01.20</span>
                  </div>
                  <div>
                    <span className="text-secondary">Environment:</span>
                    <span className="ml-2 font-mono">Development</span>
                  </div>
                  <div>
                    <span className="text-secondary">Node:</span>
                    <span className="ml-2 font-mono">Elite</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        )}
      </motion.div>

      {/* Reset Confirmation Modal */}
      <Modal
        isOpen={showResetModal}
        onClose={() => setShowResetModal(false)}
        title="Reset Settings"
        footer={
          <>
            <Button
              variant="ghost"
              onClick={() => setShowResetModal(false)}
            >
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={handleReset}
              loading={loading}
            >
              Reset All Settings
            </Button>
          </>
        }
      >
        <p className="text-gray-600 dark:text-gray-400">
          Are you sure you want to reset all settings to their default values? This action cannot be undone.
        </p>
      </Modal>
    </div>
  );
};
