import React from 'react';
import { useDarkMode } from '../../hooks/useDarkMode';
import { useMounted } from '../../hooks/useMounted';

export const ThemeTest = () => {
  const mounted = useMounted();
  const { theme, isDark, toggleTheme, systemTheme } = useDarkMode();

  if (!mounted) {
    return <div>Loading theme...</div>;
  }

  const handleToggle = () => {
    console.log('🎨 Theme toggle clicked:', {
      currentTheme: theme,
      willBe: isDark ? 'light' : 'dark'
    });
    toggleTheme();
  };

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold text-primary">Theme System Test</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Current State */}
        <div className="card p-4">
          <h3 className="text-lg font-semibold text-primary mb-2">Current State</h3>
          <div className="space-y-2 text-sm">
            <div>Theme: <span className="font-mono bg-tertiary px-2 py-1 rounded">{theme}</span></div>
            <div>Is Dark: <span className="font-mono bg-tertiary px-2 py-1 rounded">{isDark.toString()}</span></div>
            <div>System: <span className="font-mono bg-tertiary px-2 py-1 rounded">{systemTheme}</span></div>
            <div>Mounted: <span className="font-mono bg-tertiary px-2 py-1 rounded">{mounted.toString()}</span></div>
          </div>
        </div>

        {/* Test Controls */}
        <div className="card p-4">
          <h3 className="text-lg font-semibold text-primary mb-2">Test Controls</h3>
          <div className="space-y-3">
            <button
              onClick={handleToggle}
              className="btn-primary w-full"
            >
              Toggle Theme
            </button>
            <button
              onClick={() => console.log('🔍 Theme state:', { theme, isDark, systemTheme })}
              className="btn-secondary w-full"
            >
              Log State
            </button>
          </div>
        </div>
      </div>

      {/* Visual Test Elements */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-primary">Visual Elements Test</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Card Test */}
          <div className="card card-hover p-4">
            <h4 className="font-semibold text-primary">Card Component</h4>
            <p className="text-secondary mt-2">This card should adapt to theme changes.</p>
          </div>

          {/* Button Test */}
          <div className="card p-4 space-y-2">
            <h4 className="font-semibold text-primary">Button Variants</h4>
            <button className="btn-primary">Primary</button>
            <button className="btn-secondary">Secondary</button>
            <button className="btn-ghost">Ghost</button>
          </div>

          {/* Input Test */}
          <div className="card p-4">
            <h4 className="font-semibold text-primary">Input Test</h4>
            <input
              type="text"
              placeholder="Test input..."
              className="input-primary mt-2"
            />
          </div>
        </div>
      </div>

      {/* Background Test */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-primary">Background Variants</h3>
        <div className="grid grid-cols-3 gap-2 text-center text-sm">
          <div className="bg-primary p-4 rounded">Primary BG</div>
          <div className="bg-secondary p-4 rounded">Secondary BG</div>
          <div className="bg-tertiary p-4 rounded">Tertiary BG</div>
        </div>
      </div>
    </div>
  );
};
