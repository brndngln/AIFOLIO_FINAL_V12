import React, { useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDarkMode } from '../hooks/useDarkMode';
import { useToggle } from '../hooks/useToggle';
import { useClickOutside } from '../hooks/useClickOutside';
import { useMounted } from '../hooks/useMounted';

// Icons as React components for better performance
const SunIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>
);

const MoonIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
  </svg>
);

const SettingsIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

export const ThemeEditorPanel = () => {
  const mounted = useMounted();
  const { theme, isDark, toggleTheme, systemTheme } = useDarkMode();
  const [isExpanded, toggleExpanded, setExpanded] = useToggle(false);
  const panelRef = useRef(null);

  // Close panel when clicking outside
  useClickOutside(panelRef, () => setExpanded(false), isExpanded);

  // Don't render until mounted to prevent hydration mismatch
  if (!mounted) {
    return null;
  }

  const panelVariants = {
    hidden: {
      opacity: 0,
      scale: 0.95,
      y: -10,
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 30,
      },
    },
    exit: {
      opacity: 0,
      scale: 0.95,
      y: -10,
      transition: {
        duration: 0.2,
      },
    },
  };

  const buttonVariants = {
    hover: {
      scale: 1.05,
      transition: {
        type: "spring",
        stiffness: 400,
        damping: 17,
      },
    },
    tap: {
      scale: 0.95,
    },
  };

  const iconVariants = {
    rotate: {
      rotate: 360,
      transition: {
        duration: 0.6,
        ease: "easeInOut",
      },
    },
  };

  return (
    <div className="fixed top-4 right-4 z-50" ref={panelRef}>
      {/* Toggle Button */}
      <motion.button
        variants={buttonVariants}
        whileHover="hover"
        whileTap="tap"
        onClick={toggleExpanded}
        className={`
          relative p-3 rounded-full shadow-lg backdrop-blur-sm border
          transition-all duration-300 ease-in-out
          ${isDark
            ? 'bg-gray-800/90 border-gray-700 text-yellow-400 hover:bg-gray-700/90'
            : 'bg-white/90 border-gray-200 text-gray-700 hover:bg-gray-50/90'
          }
          hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2
          ${isDark ? 'focus:ring-yellow-400' : 'focus:ring-blue-500'}
        `}
        aria-label="Toggle theme settings"
      >
        <motion.div
          variants={iconVariants}
          animate={isExpanded ? "rotate" : ""}
        >
          {isExpanded ? <SettingsIcon /> : isDark ? <MoonIcon /> : <SunIcon />}
        </motion.div>
      </motion.button>

      {/* Expanded Panel */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            variants={panelVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            className={`
              absolute top-16 right-0 min-w-[280px] p-4 rounded-xl shadow-xl
              backdrop-blur-sm border transition-colors duration-300
              ${isDark
                ? 'bg-gray-800/95 border-gray-700'
                : 'bg-white/95 border-gray-200'
              }
            `}
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <h3 className={`font-semibold text-lg ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Theme Settings
              </h3>
              <div className={`text-sm px-2 py-1 rounded-full ${
                isDark
                  ? 'bg-yellow-400/20 text-yellow-400'
                  : 'bg-blue-500/20 text-blue-600'
              }`}>
                {theme}
              </div>
            </div>

            {/* Theme Toggle */}
            <div className="space-y-3">
              <motion.button
                variants={buttonVariants}
                whileHover="hover"
                whileTap="tap"
                onClick={toggleTheme}
                className={`
                  w-full flex items-center justify-between p-3 rounded-lg
                  transition-all duration-300 border
                  ${isDark
                    ? 'bg-gray-700/50 border-gray-600 hover:bg-gray-600/50'
                    : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                  }
                  focus:outline-none focus:ring-2 focus:ring-offset-2
                  ${isDark ? 'focus:ring-yellow-400' : 'focus:ring-blue-500'}
                `}
              >
                <div className="flex items-center space-x-3">
                  <motion.div
                    animate={{ rotate: isDark ? 0 : 180 }}
                    transition={{ duration: 0.5, ease: "easeInOut" }}
                  >
                    {isDark ? <MoonIcon /> : <SunIcon />}
                  </motion.div>
                  <span className={`font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {isDark ? 'Dark Mode' : 'Light Mode'}
                  </span>
                </div>

                {/* Toggle Switch */}
                <div className={`
                  relative w-12 h-6 rounded-full transition-colors duration-300
                  ${isDark ? 'bg-yellow-400' : 'bg-gray-300'}
                `}>
                  <motion.div
                    className="absolute top-1 w-4 h-4 bg-white rounded-full shadow-sm"
                    animate={{ x: isDark ? 24 : 2 }}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                </div>
              </motion.button>

              {/* System Theme Info */}
              <div className={`text-sm p-3 rounded-lg border ${
                isDark
                  ? 'bg-gray-700/30 border-gray-600 text-gray-300'
                  : 'bg-gray-50 border-gray-200 text-gray-600'
              }`}>
                <div className="flex items-center justify-between">
                  <span>System preference:</span>
                  <span className="font-medium capitalize">{systemTheme}</span>
                </div>
              </div>

              {/* Status Indicator */}
              <div className={`text-xs text-center py-2 ${
                isDark ? 'text-gray-400' : 'text-gray-500'
              }`}>
                Theme persisted in localStorage
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
