import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useMounted } from '../hooks/useMounted';
import { useDarkMode } from '../hooks/useDarkMode';

interface NavbarProps {
  currentRoute?: string;
  onMenuToggle?: () => void;
  isSidebarOpen?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentRoute = '/',
  onMenuToggle,
  isSidebarOpen = false
}) => {
  const mounted = useMounted();
  const { isDark } = useDarkMode();
  const [routeTitle, setRouteTitle] = useState('AIFOLIO');

  useEffect(() => {
    if (mounted) {
      // Log vault stub on mount and route changes
      console.log(`📦 VAULT: [standby] | Page: ${currentRoute}`);
      console.log('🔒 VAULT: null [standby]');

      // Set route-based title
      const titles: Record<string, string> = {
        '/': 'AIFOLIO Dashboard',
        '/dashboard': 'Control Center',
        '/vault': 'Vault [Standby]',
        '/analytics': 'Analytics Hub',
        '/settings': 'System Config',
        '/profile': 'User Profile',
      };

      setRouteTitle(titles[currentRoute] || 'AIFOLIO');
    }
  }, [mounted, currentRoute]);

  if (!mounted) {
    return <div className="h-16 bg-primary border-b border-gray-200 dark:border-gray-700" />;
  }

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="sticky top-0 z-40 w-full bg-primary/95 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700"
    >
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left Section - Menu + Title */}
          <div className="flex items-center space-x-4">
            {/* Mobile Menu Button */}
            <button
              onClick={onMenuToggle}
              className="lg:hidden p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
              aria-label="Toggle sidebar"
            >
              <motion.div
                animate={{ rotate: isSidebarOpen ? 90 : 0 }}
                transition={{ duration: 0.2 }}
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </motion.div>
            </button>

            {/* Title Section */}
            <div className="flex items-center space-x-3">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex items-center space-x-2"
              >
                <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">AI</span>
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-lg font-semibold text-primary">{routeTitle}</h1>
                  <p className="text-xs text-secondary">Elite Portfolio System</p>
                </div>
              </motion.div>
            </div>
          </div>

          {/* Center Section - Route Context */}
          <div className="hidden md:flex items-center space-x-2">
            <span className="text-sm text-secondary">Route:</span>
            <code className="px-2 py-1 bg-tertiary rounded text-xs font-mono text-primary">
              {currentRoute}
            </code>
          </div>

          {/* Right Section - Vault Placeholder + Status */}
          <div className="flex items-center space-x-4">
            {/* Vault Placeholder Tag */}
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="hidden sm:flex items-center space-x-2 px-3 py-1 bg-vault-100 dark:bg-vault-800 rounded-full border border-vault-200 dark:border-vault-700"
            >
              <div className="w-2 h-2 bg-vault-400 rounded-full animate-pulse" />
              <span className="text-xs font-medium text-vault-700 dark:text-vault-300">
                VAULT: STANDBY
              </span>
            </motion.div>

            {/* System Status Indicator */}
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full" />
              <span className="hidden lg:inline text-xs text-secondary">Online</span>
            </div>

            {/* Theme Indicator */}
            <div className="hidden md:flex items-center space-x-1 px-2 py-1 bg-tertiary rounded">
              <div className="w-3 h-3 rounded-full bg-current opacity-60" />
              <span className="text-xs text-secondary">
                {isDark ? 'Dark' : 'Light'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Route Context */}
      <div className="md:hidden px-4 pb-2">
        <div className="flex items-center space-x-2">
          <span className="text-xs text-secondary">Current:</span>
          <code className="px-2 py-1 bg-tertiary rounded text-xs font-mono text-primary">
            {currentRoute}
          </code>
          <div className="flex-1" />
          <div className="flex items-center space-x-1 px-2 py-1 bg-vault-100 dark:bg-vault-800 rounded">
            <div className="w-1.5 h-1.5 bg-vault-400 rounded-full animate-pulse" />
            <span className="text-xs font-medium text-vault-700 dark:text-vault-300">
              VAULT
            </span>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};
