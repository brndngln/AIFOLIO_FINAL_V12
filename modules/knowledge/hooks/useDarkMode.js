import { useState, useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage';
import { useMounted } from './useMounted';

export const useDarkMode = () => {
  const mounted = useMounted();
  const [storedTheme, setStoredTheme] = useLocalStorage('theme', 'light');
  const [theme, setTheme] = useState('light');

  // Detect system preference
  const getSystemTheme = () => {
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  };

  // Initialize theme on mount
  useEffect(() => {
    if (!mounted) return;

    const initialTheme = storedTheme || getSystemTheme();
    setTheme(initialTheme);
    applyTheme(initialTheme);
  }, [mounted, storedTheme]);

  // Apply theme to document
  const applyTheme = (newTheme) => {
    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      const body = document.body;

      // Remove existing theme classes
      root.classList.remove('light', 'dark');
      body.classList.remove('light', 'dark');

      // Add new theme class
      root.classList.add(newTheme);
      body.classList.add(newTheme);

      // Set data attribute for CSS targeting
      root.setAttribute('data-theme', newTheme);
    }
  };

  // Toggle theme function
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    setStoredTheme(newTheme);
    applyTheme(newTheme);
  };

  // Set specific theme
  const setThemeMode = (newTheme) => {
    setTheme(newTheme);
    setStoredTheme(newTheme);
    applyTheme(newTheme);
  };

  // Listen for system theme changes
  useEffect(() => {
    if (!mounted) return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e) => {
      if (!storedTheme) {
        const systemTheme = e.matches ? 'dark' : 'light';
        setTheme(systemTheme);
        applyTheme(systemTheme);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [mounted, storedTheme]);

  return {
    theme,
    isDark: theme === 'dark',
    isLight: theme === 'light',
    toggleTheme,
    setTheme: setThemeMode,
    systemTheme: getSystemTheme(),
  };
};
