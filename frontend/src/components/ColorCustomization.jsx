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
};
// Add more presets here

// Add more color properties
const additionalProperties = {
  'app': [
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
  ],
  'card': [
    { name: 'title', defaultValue: '#D2B48C' },
    { name: 'subtitle', defaultValue: '#516B51' },
    { name: 'divider', defaultValue: '#404040' },
    { name: 'icon', defaultValue: '#D2B48C' },
    { name: 'icon-hover', defaultValue: '#3D503D' }
  ],
  // Add more component properties here
};

const ColorCustomization = () => {
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

  // Track color changes with full history
  useEffect(() => {
    if (currentColor) {
      // Create new history entry
      const handleColorChange = (component, state, color) => {
        try {
            // Validate color change
            validateColorChange(color, component, state);
            
            // Check for sentience patterns
            const patterns = [component, state, color];
            if (checkForSentience(patterns)) {
                throw new Error('Suspicious color change pattern detected');
            }
            
            const newTheme = { ...theme };
            newTheme[component][state] = color;
            setTheme(newTheme);
            setCurrentColor({ component, state, color });
            
            // Update history
            const newHistory = history.slice(0, historyIndex + 1);
            newHistory.push({ component, state, color });
            setHistory(newHistory);
            setHistoryIndex(newHistory.length - 1);
            
            // Log activity
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
      };  
    }
  }, [currentColor]);

  // Enhanced undo functionality
  const undoColor = () => {
    if (historyIndex <= 0) return;
    
    // Get previous state
    const previousState = history[historyIndex - 1];
    if (!previousState) return;

    // Update color
    const newTheme = { ...theme };
    newTheme[previousState.component][previousState.state] = previousState.color;
    setTheme(newTheme);
    
    // Update history index
    setHistoryIndex(historyIndex - 1);
    
    // Log activity
    logActivity('undo', {
        component: previousState.component,
        state: previousState.state,
        color: previousState.color,
        theme: newTheme
    });
  };

  // Enhanced redo functionality
  const redoColor = () => {
    if (historyIndex >= history.length - 1) return;
    
    // Get next state
    const nextState = history[historyIndex + 1];
    if (!nextState) return;

    // Update color
    const newTheme = { ...theme };
    newTheme[nextState.component][nextState.state] = nextState.color;
    setTheme(newTheme);
    
    // Update history index
    setHistoryIndex(historyIndex + 1);
    
    // Log activity
    logActivity('redo', {
        component: nextState.component,
        state: nextState.state,
        color: nextState.color,
        theme: newTheme
    });
  };

  // Clear history
  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all color history?')) {
      setHistory([]);
      setHistoryIndex(0);
    }
  };

  // Add color picker update with history tracking
  const handleColorUpdate = (component, property, color) => {
    const newColor = { component, state: property, value: color };
    setCurrentColor(newColor);
  };

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

  const colorPresets = {
    'default': {
      app: {
        background: '#000000',
        text: '#F5EAD4',
        accent: '#2E3D2E',
        secondary: '#516B51',
        cta: '#D2B48C'
      },
      card: {
        background: '#1A1A1A',
        border: '#516B51'
      },
      button: {
        background: '#D2B48C',
        text: '#000000'
      },
      header: {
        background: '#2E3D2E',
        text: '#F5EAD4'
      }
    },
    'cyber': {
      app: {
        background: '#000000',
        text: '#00FF00',
        accent: '#00FF00',
        secondary: '#008000',
        cta: '#00FFFF'
      },
      card: {
        background: '#1A1A1A',
        border: '#00FF00'
      },
      button: {
        background: '#00FFFF',
        text: '#000000'
      },
      header: {
        background: '#00FF00',
        text: '#000000'
      }
    },
    'classic': {
      app: {
        background: '#000000',
        text: '#FFFFFF',
        accent: '#0000FF',
        secondary: '#808080',
        cta: '#FF0000'
      },
      card: {
        background: '#1A1A1A',
        border: '#808080'
      },
      button: {
        background: '#FF0000',
        text: '#000000'
      },
      header: {
        background: '#0000FF',
        text: '#FFFFFF'
      }
    },
    'neon': {
      app: {
        background: '#000000',
        text: '#FF00FF',
        accent: '#FF00FF',
        secondary: '#8B008B',
        cta: '#FF1493'
      },
      card: {
        background: '#1A1A1A',
        border: '#FF00FF'
      },
      button: {
        background: '#FF1493',
        text: '#000000'
      },
      header: {
        background: '#FF00FF',
        text: '#000000'
      }
    },
    'minimal': {
      app: {
        background: '#000000',
        text: '#FFFFFF',
        accent: '#FFFFFF',
        secondary: '#808080',
        cta: '#FFFFFF'
      },
      card: {
        background: '#1A1A1A',
        border: '#FFFFFF'
      },
      button: {
        background: '#FFFFFF',
        text: '#000000'
      },
      header: {
        background: '#FFFFFF',
        text: '#000000'
      }
    }
  };

  const applyPreset = (presetName) => {
    try {
      const preset = colorPresets[presetName];
      const patterns = Object.keys(preset).join(' ');
      
      if (checkForSentience(patterns.split(' '))) {
        throw new Error('Suspicious preset pattern detected');
      }
      
      Object.entries(preset).forEach(([component, colors]) => {
        Object.entries(colors).forEach(([property, color]) => {
          const newTheme = { ...theme };
          newTheme[component][property] = color;
          setTheme(newTheme);
        });
      });
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
        <h2 className="text-2xl font-bold" style={{
          color: 'var(--text)',
          backgroundColor: 'var(--accent)',
          padding: 'var(--spacing-md)',
          borderRadius: 'var(--border-radius-md)'
        }}>Color Customization</h2>
        <div className="flex space-x-4">
          <button
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            onClick={resetColors}
            style={{
              backgroundColor: 'var(--cta)',
              color: 'var(--text)'
            }}
          >
            Reset to Default
          </button>
          <select
            value={activePreset}
            onChange={(e) => applyPreset(e.target.value)}
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
                  key={prop.name}
                  component={component.name}
                  property={prop.name}
                  defaultValue={prop.defaultValue}
                  onChange={(color) => handleColorUpdate(component.name, prop.name, color)}
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
