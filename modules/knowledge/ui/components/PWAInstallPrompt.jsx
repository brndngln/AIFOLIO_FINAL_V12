import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export const PWAInstallPrompt = ({
  className = '',
  onInstall,
  onDismiss
}) => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showPrompt, setShowPrompt] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);

  useEffect(() => {
    // Check if already installed
    const checkInstalled = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                          window.navigator.standalone === true;
      setIsInstalled(isStandalone);
    };

    checkInstalled();

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      console.log('🔋 AIFOLIO PWA: Install prompt available');

      // Prevent Chrome 67 and earlier from automatically showing the prompt
      e.preventDefault();

      // Stash the event so it can be triggered later
      setDeferredPrompt(e);
      setShowPrompt(true);
    };

    // Listen for appinstalled event
    const handleAppInstalled = () => {
      console.log('🔋 AIFOLIO PWA: App installed successfully');
      setIsInstalled(true);
      setShowPrompt(false);
      setDeferredPrompt(null);
      onInstall?.();
    };

    // Add event listeners
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Cleanup
    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, [onInstall]);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    setIsInstalling(true);

    try {
      // Show the prompt
      await deferredPrompt.prompt();

      // Wait for the user to respond to the prompt
      const { outcome } = await deferredPrompt.userChoice;

      console.log(`🔋 AIFOLIO PWA: User response: ${outcome}`);

      if (outcome === 'accepted') {
        console.log('🔋 AIFOLIO PWA: User accepted the install prompt');
      } else {
        console.log('🔋 AIFOLIO PWA: User dismissed the install prompt');
        onDismiss?.();
      }

      // Clear the deferredPrompt
      setDeferredPrompt(null);
      setShowPrompt(false);

    } catch (error) {
      console.error('🔋 AIFOLIO PWA: Install prompt failed:', error);
    } finally {
      setIsInstalling(false);
    }
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    onDismiss?.();
  };

  // Don't show if already installed or no prompt available
  if (isInstalled || !showPrompt || !deferredPrompt) {
    return null;
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 100, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 100, scale: 0.9 }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 30
        }}
        className={`fixed bottom-4 right-4 z-50 ${className}`}
      >
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 p-6 max-w-sm backdrop-blur-lg bg-opacity-95 dark:bg-opacity-95">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📱</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  Install AIFOLIO
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Add to home screen
                </p>
              </div>
            </div>

            <button
              onClick={handleDismiss}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              aria-label="Dismiss install prompt"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Features */}
          <div className="space-y-2 mb-6">
            <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <span className="w-4 h-4 text-green-500">✓</span>
              <span>Works offline</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <span className="w-4 h-4 text-green-500">✓</span>
              <span>Fast loading</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <span className="w-4 h-4 text-green-500">✓</span>
              <span>Native app experience</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleInstallClick}
              disabled={isInstalling}
              className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2.5 rounded-xl font-medium text-sm hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {isInstalling ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Installing...</span>
                </>
              ) : (
                <>
                  <span>📱</span>
                  <span>Install</span>
                </>
              )}
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleDismiss}
              className="px-4 py-2.5 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 font-medium text-sm transition-colors"
            >
              Later
            </motion.button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

// Hook for PWA installation status
export const usePWAInstall = () => {
  const [isInstalled, setIsInstalled] = useState(false);
  const [canInstall, setCanInstall] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);

  useEffect(() => {
    // Check if already installed
    const checkInstalled = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                          window.navigator.standalone === true;
      setIsInstalled(isStandalone);
    };

    checkInstalled();

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setCanInstall(true);
    };

    // Listen for appinstalled event
    const handleAppInstalled = () => {
      setIsInstalled(true);
      setCanInstall(false);
      setDeferredPrompt(null);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const install = async () => {
    if (!deferredPrompt) return false;

    try {
      await deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;

      setDeferredPrompt(null);
      setCanInstall(false);

      return outcome === 'accepted';
    } catch (error) {
      console.error('PWA install failed:', error);
      return false;
    }
  };

  return {
    isInstalled,
    canInstall,
    install
  };
};

export default PWAInstallPrompt;
