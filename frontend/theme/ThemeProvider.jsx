// [WINDSURF FIXED ✅]
import React, { useState, useEffect, createContext, useContext } from 'react';
import PropTypes from 'prop-types';

export const ThemeContext = createContext();

// Utility to get all default colors from ColorCustomization's components structure
function getAllDefaultColors() {
  // This structure must match the one in ColorCustomization.jsx
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
    }
    // Add more components if needed
  ];
  const customColors = {};
  components.forEach(comp => {
    customColors[comp.name] = {};
    comp.properties.forEach(prop => {
      customColors[comp.name][prop.name] = prop.defaultValue;
    });
  });
  return customColors;
}

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState({
    mode: 'dark',
    customColors: getAllDefaultColors()
  });

  useEffect(() => {
    // Set dark theme as default
    setTheme({
      mode: 'dark',
      customColors: getAllDefaultColors()
    });
    localStorage.setItem('theme', JSON.stringify({
      mode: 'dark',
      customColors: getAllDefaultColors()
    }));
    document.documentElement.setAttribute('data-theme', 'dark');
  }, []);

  const updateColor = (component, property, color) => {
    setTheme(prev => ({
      ...prev,
      customColors: {
        ...prev.customColors,
        [component]: {
          ...(prev.customColors?.[component] || {}),
          [property]: color
        }
      }
    }));
  };

  return (
    <ThemeContext.Provider value={{
      theme,
      setTheme,
      updateColor
    }}>
      {children}
    </ThemeContext.Provider>
  );
};

ThemeProvider.propTypes = {
  children: PropTypes.node.isRequired
};

export default ThemeProvider;

// Custom hook to use theme
export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
