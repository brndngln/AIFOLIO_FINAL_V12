import React, { useState, useEffect } from 'react';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import ColorCustomization from './components/ColorCustomization';
import ColorSchemeManager from './components/ColorSchemeManager';
import ThemeProvider from '../theme/ThemeProvider.jsx';
import Login from './components/Login';
import GumroadIntegrationPanel from './components/GumroadIntegrationPanel';

// Utility to load vault data from public (stub for real API)
function loadLatestVault() {
  // In a real app, fetch from backend or API
  try {
    // eslint-disable-next-line no-undef
    const preview = require('../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/vault_preview.json');
    // eslint-disable-next-line no-undef
    const metadata = require('../vaults/the_ultimate_guide_to_ai_tools_and_automation_success/metadata.json');
    return { preview, metadata };
  } catch (e) {
    return null;
  }
}


function App() {
  const vault = loadLatestVault();
  // Admin action stubs
  const handleApprove = (vault) => {
    alert('Vault approved for Gumroad!');
  };
  const handleOverridePrice = (price) => {
    alert('Override price set to $' + price);
  };
  return (
    <ThemeProvider>
      <div className="min-h-screen" style={{
        backgroundColor: 'var(--bg)',
        color: 'var(--text)'
      }}>
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold" style={{
              color: 'var(--text)',
              backgroundColor: 'var(--accent)',
              padding: 'var(--spacing-md)',
              borderRadius: 'var(--border-radius-md)',
              boxShadow: 'var(--shadow-sm)'
            }}>AIFOLIO™</h1>
            <div className="flex space-x-4">
              <button className="theme-button">
                Theme
              </button>
              <button className="theme-button">
                Settings
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Analytics Dashboard</h2>
              <AnalyticsDashboard />
            </div>
            <div className="theme-panel col-span-2">
              <GumroadIntegrationPanel
                vault={vault}
                onApprove={handleApprove}
                onOverridePrice={handleOverridePrice}
              />
            </div>
          </div>

          {/* Reserved for future features: analytics, performance, AI/screenshot enhancements */}
          {/*
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Analytics & Performance (Coming Soon)</h2>
            </div>
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>AI/Screenshot Enhancements (Coming Soon)</h2>
            </div>
          </div>
          */}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
