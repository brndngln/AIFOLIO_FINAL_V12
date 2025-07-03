import React, { useState, useEffect, createContext, useContext } from 'react';

export const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState({
    mode: 'dark',
    customColors: {}
  });

  useEffect(() => {
    // Set dark theme as default
    setTheme({
      mode: 'dark',
      customColors: {}
    });
    localStorage.setItem('theme', JSON.stringify({
      mode: 'dark',
      customColors: {}
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
      updateColor
    }}>
      {children}
    </ThemeContext.Provider>
  );
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
