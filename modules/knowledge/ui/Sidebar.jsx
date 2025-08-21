import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMounted } from '../hooks/useMounted';
import { useClickOutside } from '../hooks/useClickOutside';

export const Sidebar = ({
  isOpen,
  onClose,
  currentRoute = '/'
}) => {
  const mounted = useMounted();
  const sidebarRef = useRef(null);

  useClickOutside(
    sidebarRef,
    () => {
      if (window.innerWidth < 1024) { // Only auto-close on mobile/tablet
        onClose();
      }
    },
    isOpen // Only attach listener when sidebar is open
  );

  useEffect(() => {
    if (mounted && isOpen) {
      console.log('🔧 Sidebar: Expanded | Route:', currentRoute);
    }
  }, [mounted, isOpen, currentRoute]);

  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      route: '/dashboard',
      isActive: currentRoute === '/dashboard',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v10a2 2 0 01-2 2H10a2 2 0 01-2-2V5z" />
        </svg>
      ),
    },
    {
      id: 'vault',
      label: 'Vault',
      route: '/vault',
      isActive: currentRoute === '/vault',
      badge: 'STANDBY',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
    },
    {
      id: 'analytics',
      label: 'Analytics',
      route: '/analytics',
      isActive: currentRoute === '/analytics',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
    },
    {
      id: 'automation',
      label: 'Automation',
      route: '/automation',
      isActive: currentRoute === '/automation',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
    },
    {
      id: 'settings',
      label: 'Settings',
      route: '/settings',
      isActive: currentRoute === '/settings',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
        </svg>
      ),
    },
  ];

  if (!mounted) {
    return null;
  }

  return (
    <>
      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm lg:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        ref={sidebarRef}
        initial={{ x: -280 }}
        animate={{ x: isOpen ? 0 : -280 }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 30,
          mass: 0.8
        }}
        className="fixed top-16 left-0 z-40 w-64 h-[calc(100vh-4rem)] bg-secondary border-r border-gray-200 dark:border-gray-700 lg:translate-x-0 lg:static lg:z-auto"
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-primary">Navigation</h2>
              <button
                onClick={onClose}
                className="lg:hidden p-1 rounded text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Menu Items */}
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-thin">
            {menuItems.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <button
                  className={`
                    w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-all duration-200
                    ${item.isActive
                      ? 'bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300 border border-primary-200 dark:border-primary-800'
                      : 'text-secondary hover:bg-tertiary hover:text-primary'
                    }
                  `}
                  onClick={() => {
                    console.log(`🔗 Navigate to: ${item.route}`);
                    if (window.innerWidth < 1024) {
                      onClose();
                    }
                  }}
                >
                  <span className={item.isActive ? 'text-primary-600 dark:text-primary-400' : ''}>
                    {item.icon}
                  </span>
                  <span className="font-medium">{item.label}</span>
                  {item.badge && (
                    <span className="ml-auto px-2 py-0.5 text-xs font-medium bg-vault-100 dark:bg-vault-800 text-vault-700 dark:text-vault-300 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </button>
              </motion.div>
            ))}
          </nav>

          {/* Vault Toggle Section */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center space-x-3 px-3 py-3 bg-vault-50 dark:bg-vault-900/50 border border-vault-200 dark:border-vault-700 rounded-lg hover:bg-vault-100 dark:hover:bg-vault-800/50 transition-colors duration-200"
              onClick={() => {
                console.log('📦 VAULT: Toggle attempted [PLACEHOLDER]');
                console.log('🔒 VAULT: Access denied - System in standby mode');
              }}
            >
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-vault-400 rounded-full animate-pulse" />
                <svg className="w-5 h-5 text-vault-600 dark:text-vault-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div className="flex-1 text-left">
                <div className="text-sm font-medium text-vault-700 dark:text-vault-300">
                  Vault Control
                </div>
                <div className="text-xs text-vault-500 dark:text-vault-500">
                  Standby Mode
                </div>
              </div>
              <svg className="w-4 h-4 text-vault-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </motion.button>
          </div>
        </div>
      </motion.aside>
    </>
  );
};
