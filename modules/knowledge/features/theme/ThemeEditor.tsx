/**
 * AIFOLIO™ Theme Editor Panel
 * Elite modular architecture - Advanced theme customization
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useGlobalState } from '../../hooks/common/useGlobalState';
import { useToggle } from '../../hooks/common/useToggle';
import { useClickOutside } from '../../hooks/ui/useClickOutside';

interface ColorPreset {
  name: string;
  primary: string;
  accent: string;
  description: string;
}

const colorPresets: ColorPreset[] = [
  {
    name: 'AIFOLIO Elite',
    primary: '#6366f1',
    accent: '#f59e0b',
    description: 'Default elite theme'
  },
  {
    name: 'Ocean Depth',
    primary: '#0ea5e9',
    accent: '#06b6d4',
    description: 'Deep blue professional'
  },
  {
    name: 'Forest Empire',
    primary: '#059669',
    accent: '#84cc16',
    description: 'Nature-inspired growth'
  },
  {
    name: 'Royal Purple',
    primary: '#7c3aed',
    accent: '#a855f7',
    description: 'Luxury and sophistication'
  },
  {
    name: 'Sunset Glow',
    primary: '#ea580c',
    accent: '#f97316',
    description: 'Warm and energetic'
  },
  {
    name: 'Midnight Steel',
    primary: '#475569',
    accent: '#64748b',
    description: 'Professional minimalist'
  }
];

export function ThemeEditor() {
  const { theme, updateTheme, isDarkMode } = useGlobalState();
  const [isOpen, { toggle: togglePanel }] = useToggle(false);
  const [selectedPreset, setSelectedPreset] = useState<ColorPreset | null>(null);
  const [customColors, setCustomColors] = useState({
    primary: theme.primaryColor,
    accent: theme.accentColor
  });

  const panelRef = useClickOutside<HTMLDivElement>(() => {
    if (isOpen) togglePanel();
  });

  const applyPreset = (preset: ColorPreset) => {
    setSelectedPreset(preset);
    setCustomColors({
      primary: preset.primary,
      accent: preset.accent
    });
    updateTheme({
      primaryColor: preset.primary,
      accentColor: preset.accent
    });
  };

  const applyCustomColors = () => {
    updateTheme({
      primaryColor: customColors.primary,
      accentColor: customColors.accent
    });
  };

  const resetToDefault = () => {
    const defaultPreset = colorPresets[0];
    applyPreset(defaultPreset);
  };

  return (
    <>
      {/* Theme Editor Toggle Button */}
      <motion.button
        onClick={togglePanel}
        className={`
          fixed bottom-6 right-6 z-40
          w-14 h-14 rounded-full
          bg-gradient-to-r from-primary-500 to-accent-500
          text-white shadow-lg hover:shadow-xl
          flex items-center justify-center
          transition-all duration-300
          ${isOpen ? 'rotate-45' : 'hover:scale-110'}
        `}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        title="Theme Editor"
      >
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v6a2 2 0 002 2h4a2 2 0 002-2V5zM21 15a2 2 0 00-2-2h-4a2 2 0 00-2 2v2a2 2 0 002 2h4a2 2 0 002-2v-2z" />
        </svg>
      </motion.button>

      {/* Theme Editor Panel */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 z-30"
            />

            {/* Panel */}
            <motion.div
              ref={panelRef}
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className={`
                fixed top-0 right-0 h-full w-96 z-40
                bg-white dark:bg-gray-800
                shadow-2xl border-l border-gray-200 dark:border-gray-700
                overflow-y-auto
              `}
            >
              <div className="p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    🎨 Theme Editor
                  </h2>
                  <button
                    onClick={togglePanel}
                    className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {/* Current Theme Preview */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                    Current Theme
                  </h3>
                  <div className="p-4 rounded-lg border border-gray-200 dark:border-gray-600">
                    <div className="flex items-center space-x-4">
                      <div
                        className="w-8 h-8 rounded-full"
                        style={{ backgroundColor: theme.primaryColor }}
                      />
                      <div
                        className="w-8 h-8 rounded-full"
                        style={{ backgroundColor: theme.accentColor }}
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {isDarkMode ? 'Dark' : 'Light'} Mode
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          Primary: {theme.primaryColor} • Accent: {theme.accentColor}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Color Presets */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                    Color Presets
                  </h3>
                  <div className="space-y-2">
                    {colorPresets.map((preset) => (
                      <motion.button
                        key={preset.name}
                        onClick={() => applyPreset(preset)}
                        className={`
                          w-full p-3 rounded-lg border transition-all
                          ${selectedPreset?.name === preset.name
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                          }
                        `}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <div className="flex items-center space-x-3">
                          <div className="flex space-x-1">
                            <div
                              className="w-4 h-4 rounded-full"
                              style={{ backgroundColor: preset.primary }}
                            />
                            <div
                              className="w-4 h-4 rounded-full"
                              style={{ backgroundColor: preset.accent }}
                            />
                          </div>
                          <div className="flex-1 text-left">
                            <p className="font-medium text-gray-900 dark:text-white">
                              {preset.name}
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {preset.description}
                            </p>
                          </div>
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>

                {/* Custom Colors */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                    Custom Colors
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        Primary Color
                      </label>
                      <div className="flex items-center space-x-3">
                        <input
                          type="color"
                          value={customColors.primary}
                          onChange={(e) => setCustomColors(prev => ({ ...prev, primary: e.target.value }))}
                          className="w-12 h-10 rounded border border-gray-300 dark:border-gray-600"
                        />
                        <input
                          type="text"
                          value={customColors.primary}
                          onChange={(e) => setCustomColors(prev => ({ ...prev, primary: e.target.value }))}
                          className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="#6366f1"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                        Accent Color
                      </label>
                      <div className="flex items-center space-x-3">
                        <input
                          type="color"
                          value={customColors.accent}
                          onChange={(e) => setCustomColors(prev => ({ ...prev, accent: e.target.value }))}
                          className="w-12 h-10 rounded border border-gray-300 dark:border-gray-600"
                        />
                        <input
                          type="text"
                          value={customColors.accent}
                          onChange={(e) => setCustomColors(prev => ({ ...prev, accent: e.target.value }))}
                          className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                          placeholder="#f59e0b"
                        />
                      </div>
                    </div>

                    <motion.button
                      onClick={applyCustomColors}
                      className="w-full py-2 px-4 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      Apply Custom Colors
                    </motion.button>
                  </div>
                </div>

                {/* Actions */}
                <div className="space-y-3">
                  <motion.button
                    onClick={resetToDefault}
                    className="w-full py-2 px-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    Reset to Default
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

export default ThemeEditor;
