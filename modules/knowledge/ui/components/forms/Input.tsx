import React, { forwardRef, useState } from 'react';
import { motion } from 'framer-motion';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'filled' | 'outlined';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  label,
  error,
  helperText,
  variant = 'default',
  size = 'md',
  icon,
  iconPosition = 'left',
  loading = false,
  className = '',
  id,
  ...props
}, ref) => {
  const [isFocused, setIsFocused] = useState(false);
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-5 py-3 text-lg',
  };

  const variantClasses = {
    default: 'border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800',
    filled: 'border-0 bg-gray-100 dark:bg-gray-700',
    outlined: 'border-2 border-gray-300 dark:border-gray-600 bg-transparent',
  };

  const baseClasses = `
    w-full rounded-lg transition-all duration-200
    text-gray-900 dark:text-gray-100
    placeholder-gray-500 dark:placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
    disabled:opacity-50 disabled:cursor-not-allowed
    ${sizeClasses[size]}
    ${variantClasses[variant]}
    ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
    ${icon ? (iconPosition === 'left' ? 'pl-10' : 'pr-10') : ''}
    ${className}
  `;

  return (
    <div className="w-full">
      {/* Label */}
      {label && (
        <motion.label
          htmlFor={inputId}
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
        >
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </motion.label>
      )}

      {/* Input Container */}
      <div className="relative">
        {/* Left Icon */}
        {icon && iconPosition === 'left' && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className={`${isFocused ? 'text-primary-500' : 'text-gray-400'} transition-colors duration-200`}>
              {icon}
            </div>
          </div>
        )}

        {/* Input Field */}
        <motion.input
          ref={ref}
          id={inputId}
          className={baseClasses}
          onFocus={(e) => {
            setIsFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setIsFocused(false);
            props.onBlur?.(e);
          }}
          whileFocus={{ scale: 1.01 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          {...props}
        />

        {/* Right Icon or Loading */}
        {((icon && iconPosition === 'right') || loading) && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {loading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full"
              />
            ) : (
              <div className={`${isFocused ? 'text-primary-500' : 'text-gray-400'} transition-colors duration-200`}>
                {icon}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Helper Text or Error */}
      {(helperText || error) && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2"
        >
          {error ? (
            <p className="text-sm text-red-600 dark:text-red-400 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </p>
          ) : (
            <p className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
          )}
        </motion.div>
      )}
    </div>
  );
});

Input.displayName = 'Input';
