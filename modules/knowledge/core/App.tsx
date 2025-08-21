/**
 * AIFOLIO™ Main Application Component
 * Elite modular architecture - Root application with all integrations
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AIFOLIOApp from './init/app';
import ThemeProvider from '../ui/components/ThemeProvider';
import AppLayout from '../layouts/main/AppLayout';
import ThemeEditor from '../features/theme/ThemeEditor';
import LoadingSpinner from '../ui/components/LoadingSpinner';
import { useGlobalState } from '../hooks/common/useGlobalState';

// Initialize the AIFOLIO core application
const aifolioApp = AIFOLIOApp.getInstance();

function AppContent() {
  const { isLoading, user, isAuthenticated } = useGlobalState();
  const [initializationComplete, setInitializationComplete] = useState(false);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        await aifolioApp.initialize();
        setInitializationComplete(true);
      } catch (error) {
        console.error('Failed to initialize AIFOLIO application:', error);
        // Handle initialization error - could show error page
      }
    };

    initializeApp();
  }, []);

  // Show loading screen during initialization
  if (!initializationComplete) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-2xl">A</span>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">AIFOLIO™</h1>
            <p className="text-gray-400">Elite AI-Powered Digital Product Empire</p>
          </div>
          <LoadingSpinner
            size="lg"
            variant="spinner"
            color="primary"
            text="Initializing Elite Systems..."
          />
        </div>
      </div>
    );
  }

  return (
    <AppLayout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl p-8 text-white">
          <h1 className="text-4xl font-bold mb-4">
            Welcome to AIFOLIO™ Elite
          </h1>
          <p className="text-xl opacity-90 mb-6">
            Your AI-Powered Digital Product Empire Platform
          </p>
          <div className="flex flex-wrap gap-4">
            <div className="bg-white bg-opacity-20 rounded-lg p-4">
              <h3 className="font-semibold mb-1">🏦 Vaults Created</h3>
              <p className="text-2xl font-bold">0</p>
            </div>
            <div className="bg-white bg-opacity-20 rounded-lg p-4">
              <h3 className="font-semibold mb-1">💰 Revenue Generated</h3>
              <p className="text-2xl font-bold">$0</p>
            </div>
            <div className="bg-white bg-opacity-20 rounded-lg p-4">
              <h3 className="font-semibold mb-1">📈 Conversion Rate</h3>
              <p className="text-2xl font-bold">0%</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-lg flex items-center justify-center mr-4">
                <span className="text-2xl">🏦</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Create Vault
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Build your digital empire
                </p>
              </div>
            </div>
            <button className="w-full py-2 px-4 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
              Get Started
            </button>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-accent-100 dark:bg-accent-900 rounded-lg flex items-center justify-center mr-4">
                <span className="text-2xl">📊</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Analytics
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Track performance
                </p>
              </div>
            </div>
            <button className="w-full py-2 px-4 bg-accent-500 text-white rounded-lg hover:bg-accent-600 transition-colors">
              View Analytics
            </button>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mr-4">
                <span className="text-2xl">⚙️</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Settings
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Customize your experience
                </p>
              </div>
            </div>
            <button className="w-full py-2 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
              Configure
            </button>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Recent Activity
          </h2>
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📝</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No activity yet
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Start creating vaults to see your activity here
            </p>
          </div>
        </div>
      </div>

      {/* Theme Editor */}
      <ThemeEditor />
    </AppLayout>
  );
}

export function App() {
  return (
    <Router>
      <ThemeProvider defaultTheme="dark">
        <div className="App">
          <AppContent />
        </div>
      </ThemeProvider>
    </Router>
  );
}

export default App;
