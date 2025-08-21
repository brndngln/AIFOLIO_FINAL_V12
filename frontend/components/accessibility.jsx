"""Accessibility utilities for AIFOLIO.

This module provides comprehensive accessibility enhancements including
ARIA support, keyboard navigation, and screen reader optimization.
"""

import React from 'react';

// Focus management hook
export const useFocusManagement = () => {
  const focusRing = React.useRef(null);
  
  const setFocusRing = React.useCallback((element) => {
    if (focusRing.current) {
      focusRing.current.focus();
    }
  }, []);
  
  return { focusRing, setFocusRing };
};

// Keyboard navigation hook
export const useKeyboardNavigation = (onEnter, onEscape) => {
  const handleKeyDown = React.useCallback((event) => {
    switch (event.key) {
      case 'Enter':
        if (onEnter) onEnter(event);
        break;
      case 'Escape':
        if (onEscape) onEscape(event);
        break;
      default:
        break;
    }
  }, [onEnter, onEscape]);
  
  return { handleKeyDown };
};

// Screen reader announcements
export const announceToScreenReader = (message, priority = 'polite') => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;
  
  document.body.appendChild(announcement);
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

// Accessible button component
export const AccessibleButton = ({ 
  children, 
  onClick, 
  disabled = false, 
  ariaLabel, 
  variant = 'primary',
  size = 'md',
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 disabled:pointer-events-none disabled:opacity-50';
  
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    outline: 'border border-gray-300 bg-transparent hover:bg-gray-50'
  };
  
  const sizes = {
    sm: 'h-8 px-3 text-sm',
    md: 'h-10 px-4',
    lg: 'h-12 px-6 text-lg'
  };
  
  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      {...props}
    >
      {children}
    </button>
  );
};

// Accessible form input
export const AccessibleInput = ({ 
  label, 
  error, 
  required = false, 
  type = 'text',
  ...props 
}) => {
  const id = React.useId();
  const errorId = `${id}-error`;
  
  return (
    <div className="space-y-2">
      <label 
        htmlFor={id} 
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        id={id}
        type={type}
        className={`block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : undefined}
        {...props}
      />
      {error && (
        <p id={errorId} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

// Skip navigation link
export const SkipNavigation = () => (
  <a
    href="#main-content"
    className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary-600 text-white px-4 py-2 rounded-md z-50"
  >
    Skip to main content
  </a>
);

// Loading indicator with proper ARIA
export const AccessibleLoader = ({ message = "Loading..." }) => (
  <div 
    role="status" 
    aria-live="polite" 
    className="flex items-center justify-center p-4"
  >
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    <span className="sr-only">{message}</span>
  </div>
);
