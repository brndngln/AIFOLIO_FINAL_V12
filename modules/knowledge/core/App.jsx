// 🔄 Auto-rewritten by Windsurf Repairer

import React, { useState, useEffect } from 'react';
import { AppWrapper } from '../layouts/AppWrapper';
import { motion } from 'framer-motion';

function App() {
  const [currentRoute, setCurrentRoute] = useState('/');

  // Simulate route detection (in real app, this would come from router)
  useEffect(() => {
    const path = window.location.pathname || '/';
    setCurrentRoute(path);

    // Log initial app load
    console.log('🚀 AIFOLIO App: Initialized');
    console.log('📍 Initial Route:', path);
  }, []);

  return (
    <AppWrapper currentRoute={currentRoute}>
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-6 max-w-4xl mx-auto">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl font-bold text-primary"
          >
            AIFOLIO Elite System
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-secondary"
          >
            Phase 1.3: Intelligent Layout Fusion + AppWrapper Control Grid
          </motion.p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
            {/* System Status Card */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="card card-hover p-6"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                <h3 className="text-lg font-semibold text-primary">System Status</h3>
              </div>
              <p className="text-sm text-secondary mb-2">✅ Theme System: Operational</p>
              <p className="text-sm text-secondary mb-2">✅ Layout Fusion: Active</p>
              <p className="text-sm text-secondary mb-2">✅ Responsive Design: Enabled</p>
              <p className="text-sm text-secondary">✅ Vault Integration: Standby</p>
            </motion.div>

            {/* Navigation Info Card */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="card card-hover p-6"
            >
              <div className="flex items-center space-x-3 mb-4">
                <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
                <h3 className="text-lg font-semibold text-primary">Navigation</h3>
              </div>
              <p className="text-sm text-secondary mb-2">📱 Mobile: Collapsible sidebar</p>
              <p className="text-sm text-secondary mb-2">💻 Desktop: Auto-expanded</p>
              <p className="text-sm text-secondary mb-2">🎯 Route: {currentRoute}</p>
              <p className="text-sm text-secondary">🔧 Click menu to test sidebar</p>
            </motion.div>

            {/* Vault Status Card */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="card card-hover p-6 md:col-span-2 lg:col-span-1"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-3 h-3 bg-vault-400 rounded-full animate-pulse" />
                <h3 className="text-lg font-semibold text-primary">Vault Control</h3>
              </div>
              <p className="text-sm text-secondary mb-2">🔒 Status: Standby Mode</p>
              <p className="text-sm text-secondary mb-2">📦 Integration: Ready</p>
              <p className="text-sm text-secondary mb-2">🎛️ Controls: Placeholder</p>
              <p className="text-sm text-secondary">⚡ Future: Agent HUD Mount</p>
            </motion.div>
          </div>

          {/* Instructions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="mt-12 p-6 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-200 dark:border-primary-800"
          >
            <h4 className="text-lg font-semibold text-primary mb-3">AppShell Control Layer Active</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-secondary">
              <div>
                <p className="mb-2">🎨 <strong>Theme Toggle:</strong> Top-right floating panel</p>
                <p className="mb-2">🧭 <strong>Navigation:</strong> Responsive navbar + sidebar</p>
              </div>
              <div>
                <p className="mb-2">📱 <strong>Mobile:</strong> Collapsible menu with overlay</p>
                <p className="mb-2">🔍 <strong>Console:</strong> Check logs for vault status</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </AppWrapper>
  );
}

export default App;
