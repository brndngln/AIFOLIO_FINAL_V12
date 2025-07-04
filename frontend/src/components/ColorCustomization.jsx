import React, { useState, useEffect } from 'react';
import EnhancedColorPicker from './EnhancedColorPicker';
import { useTheme } from '../../theme/ThemeProvider.jsx';
import ColorPreview from './ColorPreview';
import ButtonPreview from './ButtonPreview';
// import { useEthicalMonitor } from '../utils/EthicalMonitor'; // (Removed: file does not exist)

// Color presets for the customization system
const colorPresets = {
  matted: {
    background: '#181A17',
    text: '#E3DBC8',
    accent: '#5A695A',
    secondary: '#7A867A',
    cta: '#BBAA8E',
    border: '#7A867A'
  },
  default: {
    background: '#000000',
    text: '#F5EAD4',
    accent: '#2E3D2E',
    secondary: '#516B51',
    cta: '#D2B48C',
    border: '#516B51'
  },
  classic: {
    background: '#000000',
    text: '#FF0000',
    accent: '#0000FF',
    secondary: '#0000AA',
    cta: '#FF0000',
    border: '#0000AA'
  },
  minimal: {
    background: '#000000',
    text: '#FFFFFF',
    accent: '#FFFFFF',
    secondary: '#808080',
    cta: '#FFFFFF',
    border: '#808080'
  }
  // Add more component properties here
};

const ColorCustomization = () => {
  // ...hooks and logic above...
  // --- COMPONENTS ARRAY MOVED INSIDE FUNCTION ---
  const components = [
    {
      name: 'app',
      properties: [
        { name: 'background', defaultValue: '#000000' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'accent', defaultValue: '#2E3D2E' },
        { name: 'secondary', defaultValue: '#516B51' },
        { name: 'cta', defaultValue: '#D2B48C' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'shadow', defaultValue: 'rgba(0, 0, 0, 0.2)' },
        { name: 'hover', defaultValue: '#3D503D' },
        { name: 'active', defaultValue: '#3D503D' },
        { name: 'focus', defaultValue: '#2E3D2E' },
        { name: 'link', defaultValue: '#D2B48C' },
        { name: 'link-hover', defaultValue: '#3D503D' },
        { name: 'link-visited', defaultValue: '#516B51' },
        { name: 'error', defaultValue: '#FF0000' },
        { name: 'success', defaultValue: '#00FF00' },
        { name: 'warning', defaultValue: '#FFFF00' },
        { name: 'info', defaultValue: '#00FFFF' },
        { name: 'disabled', defaultValue: '#404040' },
        { name: 'placeholder', defaultValue: '#808080' },
        { name: 'underline', defaultValue: '#D2B48C' }
      ]
    },
    {
      name: 'card',
      properties: [
        { name: 'background', defaultValue: '#1A1A1A' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'shadow', defaultValue: 'rgba(0, 0, 0, 0.2)' },
        { name: 'hover', defaultValue: '#2E3D2E' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'active', defaultValue: '#3D503D' },
        { name: 'focus', defaultValue: '#2E3D2E' },
        { name: 'title', defaultValue: '#D2B48C' },
        { name: 'subtitle', defaultValue: '#516B51' },
        { name: 'divider', defaultValue: '#404040' },
        { name: 'icon', defaultValue: '#D2B48C' },
        { name: 'icon-hover', defaultValue: '#3D503D' }
      ]
    },
    {
      name: 'button',
      properties: [
        { name: 'background', defaultValue: '#D2B48C' },
        { name: 'text', defaultValue: '#000000' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'hover', defaultValue: '#3D503D' },
        { name: 'active', defaultValue: '#3D503D' },
        { name: 'focus', defaultValue: '#2E3D2E' },
        { name: 'disabled', defaultValue: '#404040' },
        { name: 'secondary-background', defaultValue: '#516B51' },
        { name: 'secondary-text', defaultValue: '#F5EAD4' },
        { name: 'danger-background', defaultValue: '#FF0000' },
        { name: 'danger-text', defaultValue: '#FFFFFF' },
        { name: 'loading', defaultValue: '#FFFFFF' },
        { name: 'icon', defaultValue: '#000000' },
        { name: 'icon-hover', defaultValue: '#3D503D' },
        { name: 'icon-active', defaultValue: '#2E3D2E' }
      ]
    },
    {
      name: 'input',
      properties: [
        { name: 'background', defaultValue: '#1A1A1A' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'hover', defaultValue: '#2E3D2E' },
        { name: 'focus', defaultValue: '#D2B48C' },
        { name: 'disabled', defaultValue: '#404040' },
        { name: 'placeholder', defaultValue: '#808080' },
        { name: 'error', defaultValue: '#FF0000' },
        { name: 'success', defaultValue: '#00FF00' },
        { name: 'warning', defaultValue: '#FFFF00' },
        { name: 'info', defaultValue: '#00FFFF' },
        { name: 'underline', defaultValue: '#D2B48C' },
        { name: 'underline-hover', defaultValue: '#3D503D' },
        { name: 'underline-focus', defaultValue: '#2E3D2E' }
      ]
    },
    {
      name: 'link',
      properties: [
        { name: 'text', defaultValue: '#D2B48C' },
        { name: 'hover', defaultValue: '#3D503D' },
        { name: 'visited', defaultValue: '#516B51' },
        { name: 'active', defaultValue: '#2E3D2E' },
        { name: 'underline', defaultValue: '#D2B48C' },
        { name: 'underline-hover', defaultValue: '#3D503D' },
        { name: 'underline-active', defaultValue: '#2E3D2E' }
      ]
    },
    {
      name: 'alert',
      properties: [
        { name: 'background', defaultValue: '#2E3D2E' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'icon', defaultValue: '#D2B48C' },
        { name: 'success-background', defaultValue: '#00FF00' },
        { name: 'success-text', defaultValue: '#000000' },
        { name: 'error-background', defaultValue: '#FF0000' },
        { name: 'error-text', defaultValue: '#FFFFFF' },
        { name: 'warning-background', defaultValue: '#FFFF00' },
        { name: 'warning-text', defaultValue: '#000000' },
        { name: 'info-background', defaultValue: '#00FFFF' },
        { name: 'info-text', defaultValue: '#000000' }
      ]
    },
    {
      name: 'tooltip',
      properties: [
        { name: 'background', defaultValue: '#000000' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'arrow', defaultValue: '#2E3D2E' },
        { name: 'hover', defaultValue: '#3D503D' }
      ]
    },
    {
      name: 'modal',
      properties: [
        { name: 'overlay', defaultValue: 'rgba(0, 0, 0, 0.7)' },
        { name: 'background', defaultValue: '#1A1A1A' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'header-background', defaultValue: '#2E3D2E' },
        { name: 'header-text', defaultValue: '#D2B48C' },
        { name: 'close-button', defaultValue: '#D2B48C' },
        { name: 'close-button-hover', defaultValue: '#3D503D' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'shadow', defaultValue: 'rgba(0, 0, 0, 0.3)' }
      ]
    },
    {
      name: 'header',
      properties: [
        { name: 'background', defaultValue: '#2E3D2E' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'shadow', defaultValue: 'rgba(0, 0, 0, 0.2)' },
        { name: 'logo', defaultValue: '#D2B48C' },
        { name: 'nav-link', defaultValue: '#F5EAD4' },
        { name: 'nav-link-hover', defaultValue: '#3D503D' },
        { name: 'nav-link-active', defaultValue: '#2E3D2E' }
      ]
    },
    {
      name: 'navigation',
      properties: [
        { name: 'background', defaultValue: '#1A1A1A' },
        { name: 'text', defaultValue: '#F5EAD4' },
        { name: 'border', defaultValue: '#516B51' },
        { name: 'item-hover', defaultValue: '#2E3D2E' },
        { name: 'item-active', defaultValue: '#3D503D' },
        { name: 'icon', defaultValue: '#D2B48C' },
        { name: 'icon-hover', defaultValue: '#3D503D' },
        { name: 'icon-active', defaultValue: '#2E3D2E' },
        { name: 'divider', defaultValue: '#404040' }
      ]
    }
  ];

  const [activePreset, setActivePreset] = useState('default');
  const { theme, setTheme } = useTheme();
  const [showPreview, setShowPreview] = useState(false);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [currentColor, setCurrentColor] = useState(null);

  // Ethical monitoring functions are disabled (EthicalMonitor not found)
  const validateColorChange = () => {};
  const logActivity = () => {};
  const checkForSentience = () => false;

  // Enhanced safety measures to prevent sentience
  useEffect(() => {
    const checkForSentience = () => {
      // Prevent any attempts at self-awareness
      if (theme.customColors && Object.keys(theme.customColors).length > 1000) {
        console.warn('Color system complexity limit reached. Resetting to default.');
        applyPreset('default');
      }

      // Check for pattern matching (potential AI behavior)
      const colorValues = Object.values(theme.customColors || {});
      const colorPatterns = new Set();
      
      colorValues.forEach(color => {
        if (typeof color === 'string') {
          // Check for common AI patterns
          if (color.includes('sentience') || color.includes('awareness')) {
            console.warn('Potential AI pattern detected. Resetting to default.');
            applyPreset('default');
          }
          
          // Track color patterns
          const pattern = color.replace(/[^a-zA-Z]/g, '');
          colorPatterns.add(pattern);
        }
      });

      // If too many similar patterns, reset
      if (colorPatterns.size > 500) {
        console.warn('Too many similar color patterns. Resetting to default.');
        applyPreset('default');
      }
    };

    // Check every 2 seconds
    const interval = setInterval(checkForSentience, 2000);
    return () => clearInterval(interval);
  }, []);

  // Add memory limit checker
  useEffect(() => {
    const checkMemoryUsage = () => {
      // Check if the component is using too much memory
      if (performance.memory && performance.memory.usedJSHeapSize > 100 * 1024 * 1024) {
        console.warn('Memory usage too high. Resetting to default.');
        applyPreset('default');
      }
    };

    // Check memory every 10 seconds
    const interval = setInterval(checkMemoryUsage, 10000);
    return () => clearInterval(interval);
  }, []);

  // Track color changes with full history (store entire customColors object)
  useEffect(() => {
    if (currentColor && currentColor.component && currentColor.state && currentColor.color) {
      const { component, state, color } = currentColor;
      try {
        validateColorChange(color, component, state);
        const newTheme = { ...theme, customColors: JSON.parse(JSON.stringify(theme.customColors || {})) };
        if (!newTheme.customColors[component]) newTheme.customColors[component] = {};
        newTheme.customColors[component][state] = color;
        setTheme(newTheme);
        // Truncate history if not at the end before pushing new change
        const newHistory = history.slice(0, historyIndex + 1);
        // Push a deep copy of the new customColors object
        newHistory.push(JSON.parse(JSON.stringify(newTheme.customColors)));
        setHistory(newHistory);
        setHistoryIndex(newHistory.length - 1);
        // Debug log
        console.log('[COLOR CHANGE] component:', component, 'state:', state, 'color:', color, 'theme:', newTheme.customColors, 'history:', newHistory, 'historyIndex:', newHistory.length - 1);
        logActivity('color_change', {
          component,
          state,
          color,
          theme: newTheme
        });
      } catch (error) {
        console.error('Error changing color:', error);
        throw error;
      }
    }
  }, [currentColor]);

  // On mount, record the initial theme state in history for undo (store full customColors object)
  useEffect(() => {
    const initialCustomColors = JSON.parse(JSON.stringify(theme.customColors || {}));
    setHistory([initialCustomColors]);
    setHistoryIndex(0);
  }, []);

  // Enhanced undo functionality
  const undoColor = () => {
    if (historyIndex <= 0) return;
    
    // Get previous state
    const previousState = history[historyIndex - 1];
    if (!previousState) return;

    // Restore the entire customColors object from history
    const restoredCustomColors = JSON.parse(JSON.stringify(previousState));
    setTheme({ ...theme, customColors: restoredCustomColors });

    // Update history index
    setHistoryIndex(historyIndex - 1);

    // Debug log
    console.log('[UNDO] historyIndex:', historyIndex - 1, 'restored customColors:', restoredCustomColors, 'history:', history);
    // Log activity
    logActivity('undo', {
      restoredCustomColors,
      theme: { ...theme, customColors: restoredCustomColors }
    });
  };

  // Enhanced redo functionality
  const redoColor = () => {
    if (historyIndex >= history.length - 1) return;
    
    // Get next state
    const nextState = history[historyIndex + 1];
    if (!nextState) return;

    // Restore the entire customColors object from history (deep copy)
    const restoredCustomColors = JSON.parse(JSON.stringify(nextState));
    setTheme({ ...theme, customColors: restoredCustomColors });

    // Update history index
    setHistoryIndex(historyIndex + 1);

    // Debug log
    console.log('[REDO] historyIndex:', historyIndex + 1, 'restored customColors:', restoredCustomColors, 'history:', history);
    // Log activity
    logActivity('redo', {
      restoredCustomColors,
      theme: { ...theme, customColors: restoredCustomColors }
    });
  };

  // Add color picker update with history tracking
  const handleColorUpdate = (component, property, color) => {
    setTheme(prevTheme => {
      const newTheme = { ...prevTheme, customColors: { ...prevTheme.customColors } };
      if (!newTheme.customColors[component]) newTheme.customColors[component] = {};
      newTheme.customColors[component][property] = color;
      return newTheme;
    });
    setHistory(prevHistory => {
      // Use prevTheme for the latest state, not outer closure
      const newCustomColors = JSON.parse(JSON.stringify(
        (typeof window !== 'undefined' && window.__LATEST_CUSTOM_COLORS__) || {}
      ));
      if (!newCustomColors[component]) newCustomColors[component] = {};
      newCustomColors[component][property] = color;
      const newHist = prevHistory.slice(0, historyIndex + 1);
      newHist.push(newCustomColors);
      // Set historyIndex based on newHist length
      setHistoryIndex(newHist.length - 1);
      // Save to global for next update
      if (typeof window !== 'undefined') window.__LATEST_CUSTOM_COLORS__ = newCustomColors;
      return newHist;
    });
  };

  const applyPreset = (presetName) => {
    try {
      const preset = colorPresets[presetName];
      // ... (rest of the code remains the same)
      
      if (checkForSentience(patterns.split(' '))) {
        throw new Error('Suspicious preset pattern detected');
      }
      
      // Apply flat preset to 'app' component properties
      const newTheme = { ...theme };
      Object.entries(preset).forEach(([property, color]) => {
        if (!newTheme.customColors) newTheme.customColors = {};
        if (!newTheme.customColors.app) newTheme.customColors.app = {};
        newTheme.customColors.app[property] = color;
      });
      setTheme(newTheme);
      setHistory([]);
      setHistoryIndex(-1);
      
      logActivity('preset_select', {
        preset: presetName,
        theme: preset
      });
    } catch (error) {
      console.error('Error applying preset:', error);
      throw error;
    }
  };

  const resetColors = () => {
    applyPreset('default');
  };

  return (
    <div className="theme-panel">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold" style={{ color: 'var(--text)' }}>
          Color Customization
        </h2>
        <div className="flex space-x-4">
          <button
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            onClick={resetColors}
            style={{ backgroundColor: 'var(--cta)' }}
          >
            Reset to Default
          </button>
          <button
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            onClick={undoColor}
            style={{ backgroundColor: 'var(--accent)', color: 'var(--text)' }}
            data-testid="undo-button"
          >
            Undo Last Change
          </button>
          <button
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            onClick={redoColor}
            style={{ backgroundColor: 'var(--accent)', color: 'var(--text)' }}
            data-testid="redo-button"
          >
            Redo Last Change
          </button>
          <button
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            onClick={() => setShowPreview((v) => !v)}
            style={{ backgroundColor: 'var(--accent)', color: 'var(--text)' }}
            data-testid="preview-button"
          >
            {showPreview ? 'Hide Preview' : 'Show Preview'}
          </button>
          <select
            value={activePreset}
            onChange={(e) => {
              setActivePreset(e.target.value);
              applyPreset(e.target.value);
            }}
            className="px-4 py-2 rounded"
            style={{
              backgroundColor: 'var(--card)',
              color: 'var(--text)',
              border: '1px solid var(--secondary)'
            }}
          >
            {Object.keys(colorPresets).map((preset) => (
              <option key={preset} value={preset}>
                {preset.charAt(0).toUpperCase() + preset.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>
      {showPreview && (
        <div className="my-4">
          <ColorPreview />
          <ButtonPreview />
        </div>
      )}
      <div className="space-y-6">
        {components.map((component) => (
          <div key={component.name} className="space-y-4">
            <h3 className="text-lg font-semibold" style={{
              color: 'var(--text)',
              backgroundColor: 'var(--accent)',
              padding: 'var(--spacing-sm)',
              borderRadius: 'var(--border-radius-sm)'
            }}>{component.name}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {component.properties.map((prop) => (
                <EnhancedColorPicker
                  key={`${component.name}-${prop.name}-${theme.customColors?.[component.name]?.[prop.name] || prop.defaultValue}`}
                  component={component.name}
                  property={prop.name}
                  defaultValue={prop.defaultValue}
                  onChange={(comp, prop, color) => handleColorUpdate(comp, prop, color)}
                  data-testid={`colorpicker-${component.name}-${prop.name}`}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ColorCustomization;
