import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ThemeEditorPanel } from '../ui/ThemeEditorPanel';
import { Navbar } from '../ui/Navbar';
import { Sidebar } from '../ui/Sidebar';
import { useMounted } from '../hooks/useMounted';
import { useDarkMode } from '../hooks/useDarkMode';
import { useToggle } from '../hooks/useToggle';

interface AppWrapperProps {
  children: React.ReactNode;
  currentRoute?: string;
}

export const AppWrapper: React.FC<AppWrapperProps> = ({
  children,
  currentRoute = '/'
}) => {
  const mounted = useMounted();
  const { theme } = useDarkMode();
  const [isSidebarOpen, toggleSidebar, setSidebarOpen] = useToggle(false);
  const [isDesktop, setIsDesktop] = useState(false);

  // Handle responsive behavior
  useEffect(() => {
    const handleResize = () => {
      const desktop = window.innerWidth >= 1024;
      setIsDesktop(desktop);

      // Auto-open sidebar on desktop, close on mobile
      if (desktop && !isSidebarOpen) {
        setSidebarOpen(true);
      } else if (!desktop && isSidebarOpen) {
        setSidebarOpen(false);
      }
    };

    if (mounted) {
      handleResize();
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [mounted, isSidebarOpen, setSidebarOpen]);

  // Route change logging
  useEffect(() => {
    if (mounted) {
      console.log(`📦 VAULT: [standby] | Page: ${currentRoute}`);
      console.log(`🎯 AppWrapper: Route changed to ${currentRoute}`);
      console.log(`🎨 AppWrapper: Theme = ${theme}, Sidebar = ${isSidebarOpen ? 'open' : 'closed'}`);
    }
  }, [mounted, currentRoute, theme, isSidebarOpen]);

  if (!mounted) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 animate-pulse">
        <div className="h-16 bg-gray-100 dark:bg-gray-800" />
        <div className="flex">
          <div className="hidden lg:block w-64 h-screen bg-gray-50 dark:bg-gray-800" />
          <div className="flex-1 p-8">
            <div className="space-y-4">
              <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen transition-colors duration-300 bg-primary">
      {/* Theme Editor Panel - Floating in top-right */}
      <ThemeEditorPanel />

      {/* Navigation Header */}
      <Navbar
        currentRoute={currentRoute}
        onMenuToggle={toggleSidebar}
        isSidebarOpen={isSidebarOpen}
      />

      {/* Main Layout Container */}
      <div className="flex relative">
        {/* Sidebar */}
        <Sidebar
          isOpen={isSidebarOpen}
          onClose={() => setSidebarOpen(false)}
          currentRoute={currentRoute}
        />

        {/* Main Content Area */}
        <motion.main
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className={`
            flex-1 min-h-[calc(100vh-4rem)] transition-all duration-300
            ${isDesktop && isSidebarOpen ? 'lg:ml-0' : 'ml-0'}
          `}
        >
          {/* Content Wrapper with Proper Spacing */}
          <div className="relative h-full">
            {/* Page Content */}
            <div className="p-4 sm:p-6 lg:p-8">
              {children}
            </div>

            {/* Vault Status Footer */}
            <div className="fixed bottom-4 left-4 z-30">
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="flex items-center space-x-2 px-3 py-2 bg-vault-50/90 dark:bg-vault-900/90 backdrop-blur-sm border border-vault-200 dark:border-vault-700 rounded-lg shadow-sm"
              >
                <div className="w-2 h-2 bg-vault-400 rounded-full animate-pulse" />
                <span className="text-xs font-medium text-vault-700 dark:text-vault-300">
                  VAULT: STANDBY
                </span>
                <span className="text-xs text-vault-500 dark:text-vault-500">
                  {currentRoute}
                </span>
              </motion.div>
            </div>
          </div>
        </motion.main>
      </div>
    </div>
  );
};
