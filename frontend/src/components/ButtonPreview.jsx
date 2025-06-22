import React from 'react';
import { useTheme } from '../../theme/ThemeProvider.jsx';

function ButtonPreview() {
  const { theme } = useTheme();

  return (
    <div className="theme-panel p-6" role="button-preview">
      <h3 className="text-lg font-semibold mb-4" style={{
        color: 'var(--text)',
        backgroundColor: 'var(--accent)',
        padding: 'var(--spacing-sm)',
        borderRadius: 'var(--border-radius-sm)'
      }}>Button Styles Preview</h3>

      <div className="space-y-4">
        {/* Primary Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Primary Button</p>
          <button className="preview-button">
            Click Me
          </button>
        </div>

        {/* Secondary Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Secondary Button</p>
          <button className="preview-button-secondary">
            Secondary Action
          </button>
        </div>

        {/* Danger Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Danger Button</p>
          <button className="preview-button-danger">
            Delete
          </button>
        </div>

        {/* Disabled Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Disabled Button</p>
          <button className="preview-button-disabled">
            Disabled
          </button>
        </div>

        {/* Icon Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Icon Button</p>
          <button className="preview-button-icon">
            <span className="preview-icon">🔍</span>
            <span>Search</span>
          </button>
        </div>

        {/* Loading Button */}
        <div className="space-y-2">
          <p className="text-sm font-medium" style={{ color: 'var(--text)' }}>Loading Button</p>
          <button className="preview-button-loading">
            <span className="preview-spinner"></span>
            Loading...
          </button>
        </div>
      </div>
    </div>
  );
}

export default ButtonPreview;
