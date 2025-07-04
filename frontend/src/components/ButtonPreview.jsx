import React from 'react';
import { useTheme } from '../../theme/ThemeProvider.jsx';

// Utility to convert hex to rgb
function hexToRgb(hex) {
  let c = hex.replace('#', '');
  if (c.length === 3) c = c.split('').map(x => x + x).join('');
  if (c.length !== 6) return hex;
  const num = parseInt(c, 16);
  return `rgb(${(num >> 16) & 255}, ${(num >> 8) & 255}, ${num & 255})`;
}

function ButtonPreview() {
  const { theme } = useTheme();

  return (
    <div className="theme-panel p-6" role="button-preview" style={{
      backgroundColor: hexToRgb(theme.customColors?.button?.background || '#D2B48C')
    }}>
      <h3 className="text-lg font-semibold mb-4" style={{
        color: hexToRgb(theme.customColors?.button?.text || '#000000'),
        backgroundColor: hexToRgb(theme.customColors?.button?.accent || '#2E3D2E'),
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
