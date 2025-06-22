import React, { useState, useEffect } from 'react';
import { useTheme } from '../../theme/ThemeProvider.jsx';

function ColorSchemeManager() {
  const { theme, updateColor } = useTheme();
  const [savedSchemes, setSavedSchemes] = useState([]);
  const [schemeName, setSchemeName] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem('colorSchemes');
    if (saved) {
      setSavedSchemes(JSON.parse(saved));
    }
  }, []);

  const saveCurrentScheme = () => {
    if (!schemeName.trim()) return;

    const currentScheme = Object.entries(theme.customColors).reduce((acc, [component, props]) => {
      acc[component] = Object.fromEntries(
        Object.entries(props).map(([prop, color]) => [prop, color])
      );
      return acc;
    }, {});

    const newSchemes = [...savedSchemes, {
      name: schemeName,
      colors: currentScheme
    }];

    setSavedSchemes(newSchemes);
    localStorage.setItem('colorSchemes', JSON.stringify(newSchemes));
    setSchemeName('');
  };

  const applyScheme = (scheme) => {
    Object.entries(scheme.colors).forEach(([component, colors]) => {
      Object.entries(colors).forEach(([property, color]) => {
        updateColor(component, property, color);
      });
    });
  };

  const deleteScheme = (schemeName) => {
    const newSchemes = savedSchemes.filter(scheme => scheme.name !== schemeName);
    setSavedSchemes(newSchemes);
    localStorage.setItem('colorSchemes', JSON.stringify(newSchemes));
  };

  return (
    <div className="theme-panel">
      <h2 className="text-2xl font-bold mb-4" style={{
        color: 'var(--text)',
        backgroundColor: 'var(--accent)',
        padding: 'var(--spacing-md)',
        borderRadius: 'var(--border-radius-md)'
      }}>Color Schemes</h2>

      <div className="space-y-4">
        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="Scheme name"
            value={schemeName}
            onChange={(e) => setSchemeName(e.target.value)}
            className="flex-1 px-4 py-2 rounded"
            style={{
              backgroundColor: 'var(--card)',
              color: 'var(--text)',
              border: '1px solid var(--secondary)'
            }}
          />
          <button
            onClick={saveCurrentScheme}
            className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
            style={{
              backgroundColor: 'var(--cta)',
              color: 'var(--text)'
            }}
          >
            Save Scheme
          </button>
        </div>

        <div className="space-y-4">
          {savedSchemes.map((scheme) => (
            <div key={scheme.name} className="flex justify-between items-center p-4 rounded" style={{
              backgroundColor: 'var(--card)',
              border: '1px solid var(--secondary)'
            }}>
              <span className="font-semibold" style={{ color: 'var(--text)' }}>
                {scheme.name}
              </span>
              <div className="flex space-x-2">
                <button
                  onClick={() => applyScheme(scheme)}
                  className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
                  style={{
                    backgroundColor: 'var(--cta)',
                    color: 'var(--text)'
                  }}
                >
                  Apply
                </button>
                <button
                  onClick={() => deleteScheme(scheme.name)}
                  className="px-4 py-2 rounded hover:bg-var(--accent-hover)"
                  style={{
                    backgroundColor: 'var(--secondary)',
                    color: 'var(--text)'
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ColorSchemeManager;
