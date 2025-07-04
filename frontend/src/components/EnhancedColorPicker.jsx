<<<<<<< HEAD
import React, { useState, useEffect } from 'react';
import { useTheme } from '../../theme/ThemeProvider.jsx';

function EnhancedColorPicker({ component, property, defaultValue, onChange }) {
  const { theme } = useTheme();
  const [color, setColor] = useState(defaultValue);
  const [showPreview, setShowPreview] = useState(false);

  // Get current color from theme
  useEffect(() => {
    const currentColor = theme.customColors?.[component]?.[property] || defaultValue;
    setColor(currentColor);
  }, [component, property, defaultValue, theme.customColors]);

  // Update theme when color changes
  const handleColorChange = (newColor) => {
    setColor(newColor);
    onChange(newColor);
  };

=======
import React, { useState } from 'react'; // removed useEffect as unused
import { useTheme } from '../../theme/ThemeProvider.jsx';

function EnhancedColorPicker({ component, property, defaultValue, onChange, ...props }) {
  const { theme } = useTheme();
  const [showPreview, setShowPreview] = useState(false);

  // Always derive color from theme, fallback to defaultValue, then to #000000
  let color = theme?.customColors?.[component]?.[property];
  if (typeof color !== 'string' || !color) color = defaultValue;
  if (typeof color !== 'string' || !color) color = '#000000';

  // Update theme when color changes
  const handleColorChange = (newColor) => {
    onChange(component, property, newColor);
  };


>>>>>>> omni_repair_backup_20250704_1335
  // Generate random color
  const generateRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  // Validate color input
  const validateColor = (input) => {
    // Check if it's a valid hex color
    const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
    if (hexRegex.test(input)) {
      return input;
    }
    // Check if it's a valid rgba color
    const rgbaRegex = /^rgba\(\d{1,3},\s*\d{1,3},\s*\d{1,3},\s*\d(\.\d+)?\)$/;
    if (rgbaRegex.test(input)) {
      return input;
    }
    return defaultValue;
  };

  return (
    <div className="theme-panel p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold" style={{
          color: 'var(--text)',
          backgroundColor: 'var(--accent)',
          padding: 'var(--spacing-sm)',
          borderRadius: 'var(--border-radius-sm)'
        }}>{property}</h3>
        <div className="flex space-x-2">
          <button
            className="p-2 rounded hover:bg-var(--accent-hover)"
            onClick={() => setShowPreview(!showPreview)}
            style={{
              backgroundColor: 'var(--accent)',
              color: 'var(--text)'
            }}
          >
            {showPreview ? 'Hide' : 'Preview'}
          </button>
          <button
            className="p-2 rounded hover:bg-var(--accent-hover)"
            onClick={() => handleColorChange(generateRandomColor())}
            style={{
              backgroundColor: 'var(--accent)',
              color: 'var(--text)'
            }}
          >
            Random
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {/* Color Preview */}
        {showPreview && (
          <div className="p-4 rounded-lg" style={{
            backgroundColor: color,
            border: '1px solid var(--border)'
          }}>
            <p className="text-white">Preview</p>
          </div>
        )}

        {/* Color Picker */}
        <div className="space-y-2">
          <input
            type="color"
            value={color}
            onChange={(e) => {
              console.log(`[EnhancedColorPicker] Color changed for ${component}-${property}:`, e.target.value);
              handleColorChange(e.target.value);
            }}
            className="w-full h-10 rounded"
<<<<<<< HEAD
            role={`colorpicker-${component}-${property}`}
=======
            role="colorpicker"
            {...props}
            data-testid={typeof props['data-testid'] !== 'undefined' ? props['data-testid'] : 'colorpicker'}
>>>>>>> omni_repair_backup_20250704_1335
          />
          <input
            type="text"
            value={color}
            onChange={(e) => {
              const validatedColor = validateColor(e.target.value);
              handleColorChange(validatedColor);
            }}
            className="w-full p-2 rounded"
            placeholder="Enter hex or rgba color"
          />
        </div>

        {/* Current Value */}
        <div className="flex items-center justify-between p-2 rounded bg-var(--card) border border-var(--border)">
          <span style={{ color: 'var(--text)' }}>Current Value:</span>
          <span style={{ color: 'var(--text)' }}>{color}</span>
        </div>
      </div>
    </div>
  );
}

export default EnhancedColorPicker;
