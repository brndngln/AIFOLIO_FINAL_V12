import React, { forwardRef } from 'react';
import { motion } from 'framer-motion';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined' | 'elevated' | 'glass';
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  hover?: boolean;
  loading?: boolean;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  actions?: React.ReactNode;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(({
  children,
  variant = 'default',
  padding = 'md',
  hover = false,
  loading = false,
  header,
  footer,
  actions,
  className = '',
  ...props
}, ref) => {
  const paddingClasses = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
    xl: 'p-8',
  };

  const variantClasses = {
    default: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700',
    outlined: 'bg-transparent border-2 border-gray-300 dark:border-gray-600',
    elevated: 'bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700',
    glass: 'bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-white/20 dark:border-gray-700/50',
  };

  const baseClasses = `
    rounded-lg transition-all duration-200
    ${variantClasses[variant]}
    ${hover ? 'hover:shadow-md hover:border-gray-300 dark:hover:border-gray-600 cursor-pointer' : ''}
    ${className}
  `;

  const contentClasses = `
    ${paddingClasses[padding]}
    ${loading ? 'animate-pulse' : ''}
  `;

  return (
    <motion.div
      ref={ref}
      className={baseClasses}
      whileHover={hover ? { y: -2, scale: 1.01 } : {}}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      {...props}
    >
      {/* Header */}
      {header && (
        <div className={`border-b border-gray-200 dark:border-gray-700 ${padding !== 'none' ? 'pb-4 mb-4' : ''}`}>
          {header}
        </div>
      )}

      {/* Loading Skeleton */}
      {loading ? (
        <div className={contentClasses}>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
          </div>
        </div>
      ) : (
        /* Content */
        <div className={contentClasses}>
          {children}
        </div>
      )}

      {/* Actions */}
      {actions && (
        <div className={`border-t border-gray-200 dark:border-gray-700 ${padding !== 'none' ? 'pt-4 mt-4' : ''}`}>
          <div className="flex justify-end space-x-2">
            {actions}
          </div>
        </div>
      )}

      {/* Footer */}
      {footer && (
        <div className={`border-t border-gray-200 dark:border-gray-700 ${padding !== 'none' ? 'pt-4 mt-4' : ''}`}>
          {footer}
        </div>
      )}
    </motion.div>
  );
});

Card.displayName = 'Card';

// Card Header Component
export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  actions?: React.ReactNode;
}

export const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(({
  title,
  subtitle,
  icon,
  actions,
  children,
  className = '',
  ...props
}, ref) => {
  return (
    <div
      ref={ref}
      className={`flex items-center justify-between ${className}`}
      {...props}
    >
      <div className="flex items-center space-x-3">
        {icon && (
          <div className="flex-shrink-0 text-primary-600 dark:text-primary-400">
            {icon}
          </div>
        )}
        <div>
          {title && (
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {subtitle}
            </p>
          )}
          {children}
        </div>
      </div>
      {actions && (
        <div className="flex items-center space-x-2">
          {actions}
        </div>
      )}
    </div>
  );
});

CardHeader.displayName = 'CardHeader';
