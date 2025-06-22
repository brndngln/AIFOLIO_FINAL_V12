import React from 'react';
import { useTheme } from '../../theme/ThemeProvider.jsx';

function ColorPreview() {
  const { theme } = useTheme();

  return (
    <div className="theme-panel">
      <h2 className="text-2xl font-bold mb-4" style={{
        color: 'var(--text)',
        backgroundColor: 'var(--accent)',
        padding: 'var(--spacing-md)',
        borderRadius: 'var(--border-radius-md)'
      }}>Color Preview</h2>

      <div className="space-y-6">
        {/* Button Preview */}
        <div className="space-y-2">
          <h3 className="font-semibold" style={{ color: 'var(--text)' }}>Button Styles</h3>
          <div className="flex space-x-4">
            <button className="preview-button">
              Normal
            </button>
            <button className="preview-button hover:opacity-100">
              Hover
            </button>
            <button className="preview-button opacity-50">
              Disabled
            </button>
          </div>
        </div>

        {/* Card Preview */}
        <div className="space-y-2">
          <h3 className="font-semibold" style={{ color: 'var(--text)' }}>Card Styles</h3>
          <div className="preview-card p-4">
            <p style={{ color: 'var(--text)' }}>Card content</p>
            <div className="mt-2 preview-card-hover">
              <p style={{ color: 'var(--text)' }}>Hover state</p>
            </div>
          </div>
        </div>

        {/* Input Preview */}
        <div className="space-y-2">
          <h3 className="font-semibold" style={{ color: 'var(--text)' }}>Input Styles</h3>
          <div className="flex flex-col space-y-2">
            <input type="text" placeholder="Normal input" className="preview-input" />
            <input type="text" placeholder="Focused input" className="preview-input focus:ring-2" />
            <input type="text" placeholder="Disabled input" className="preview-input opacity-50" />
          </div>
        </div>

        {/* Link Preview */}
        <div className="space-y-2">
          <h3 className="font-semibold" style={{ color: 'var(--text)' }}>Link Styles</h3>
          <div className="space-y-2">
            <a href="#" className="preview-link">Normal link</a>
            <a href="#" className="preview-link hover:opacity-100">Hover link</a>
            <a href="#" className="preview-link visited:opacity-75">Visited link</a>
          </div>
        </div>

        {/* Alert Preview */}
        <div className="space-y-2">
          <h3 className="font-semibold" style={{ color: 'var(--text)' }}>Alert Styles</h3>
          <div className="preview-alert p-4">
            <p style={{ color: 'var(--text)' }}>Alert message</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ColorPreview;
