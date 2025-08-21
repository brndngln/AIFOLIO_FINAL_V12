import React, { forwardRef } from 'react';
import { motion } from 'framer-motion';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  disabled,
  ...props
}, ref) => {
  const sizeClasses = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl',
  };

  const variantClasses = {
    primary: `
      bg-primary-600 hover:bg-primary-700 focus:ring-primary-500
      text-white border border-transparent
      shadow-sm hover:shadow-md
    `,
    secondary: `
      bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700
      text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600
      focus:ring-primary-500 shadow-sm hover:shadow-md
    `,
    ghost: `
      bg-transparent hover:bg-gray-100 dark:hover:bg-gray-800
      text-gray-700 dark:text-gray-300 border border-transparent
      focus:ring-primary-500
    `,
    danger: `
      bg-red-600 hover:bg-red-700 focus:ring-red-500
      text-white border border-transparent
      shadow-sm hover:shadow-md
    `,
    success: `
      bg-green-600 hover:bg-green-700 focus:ring-green-500
      text-white border border-transparent
      shadow-sm hover:shadow-md
    `,
  };

  const baseClasses = `
    inline-flex items-center justify-center
    font-medium rounded-lg transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    ${sizeClasses[size]}
    ${variantClasses[variant]}
    ${fullWidth ? 'w-full' : ''}
    ${className}
  `;

  const isDisabled = disabled || loading;

  return (
    <motion.button
      ref={ref}
      className={baseClasses}
      disabled={isDisabled}
      whileHover={!isDisabled ? { scale: 1.02 } : {}}
      whileTap={!isDisabled ? { scale: 0.98 } : {}}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      {...props}
    >
      {/* Loading Spinner */}
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"
        />
      )}

      {/* Left Icon */}
      {!loading && icon && iconPosition === 'left' && (
        <span className={`${children ? 'mr-2' : ''}`}>
          {icon}
        </span>
      )}

      {/* Button Text */}
      {children && (
        <span className={loading ? 'opacity-75' : ''}>
          {children}
        </span>
      )}

      {/* Right Icon */}
      {!loading && icon && iconPosition === 'right' && (
        <span className={`${children ? 'ml-2' : ''}`}>
          {icon}
        </span>
      )}
    </motion.button>
  );
});

Button.displayName = 'Button';
