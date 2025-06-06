import React from 'react';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import SettingsPanel from './components/SettingsPanel';
import UserControlUI from './components/UserControlUI';
import ColorCustomization from './components/ColorCustomization';
import ColorSchemeManager from './components/ColorSchemeManager';
import { ThemeProvider } from '../theme/ThemeProvider';

function App() {
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
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Settings Panel</h2>
              <SettingsPanel />
            </div>
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Color Customization</h2>
              <ColorCustomization />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
            <div className="theme-panel">
              <h2 className="text-2xl font-bold mb-4" style={{
                color: 'var(--text)',
                backgroundColor: 'var(--accent)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--border-radius-md)'
              }}>Color Schemes</h2>
              <ColorSchemeManager />
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}
}

export default App
