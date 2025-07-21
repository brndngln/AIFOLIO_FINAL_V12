import React, { forwardRef } from 'react';
import { motion } from 'framer-motion';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  rounded?: boolean;
  dot?: boolean;
  icon?: React.ReactNode;
  removable?: boolean;
  onRemove?: () => void;
}

export const Badge = forwardRef<HTMLSpanElement, BadgeProps>(({
  children,
  variant = 'default',
  size = 'sm',
  rounded = false,
  dot = false,
  icon,
  removable = false,
  onRemove,
  className = '',
  ...props
}, ref) => {
  const sizeClasses = {
    xs: 'px-1.5 py-0.5 text-xs',
    sm: 'px-2 py-1 text-xs',
    md: 'px-2.5 py-1.5 text-sm',
    lg: 'px-3 py-2 text-base',
  };

  const variantClasses = {
    default: 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200',
    primary: 'bg-primary-100 dark:bg-primary-900/50 text-primary-800 dark:text-primary-200',
    secondary: 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300',
    success: 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200',
    warning: 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200',
    danger: 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200',
    info: 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200',
  };

  const baseClasses = `
    inline-flex items-center font-medium
    ${rounded ? 'rounded-full' : 'rounded'}
    ${dot ? 'w-2 h-2 p-0' : sizeClasses[size]}
    ${variantClasses[variant]}
    ${className}
  `;

  if (dot) {
    return (
      <motion.span
        ref={ref}
        className={baseClasses}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
        {...props}
      />
    );
  }

  return (
    <motion.span
      ref={ref}
      className={baseClasses}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: "spring", stiffness: 500, damping: 30 }}
      {...props}
    >
      {/* Icon */}
      {icon && (
        <span className={`${children ? 'mr-1' : ''} flex-shrink-0`}>
          {icon}
        </span>
      )}

      {/* Content */}
      {children && <span>{children}</span>}

      {/* Remove Button */}
      {removable && (
        <motion.button
          onClick={(e) => {
            e.stopPropagation();
            onRemove?.();
          }}
          className={`${children || icon ? 'ml-1' : ''} flex-shrink-0 hover:bg-black/10 dark:hover:bg-white/10 rounded-full p-0.5 transition-colors duration-150`}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </motion.button>
      )}
    </motion.span>
  );
});

Badge.displayName = 'Badge';

// Status Badge Component for common status indicators
export interface StatusBadgeProps extends Omit<BadgeProps, 'variant'> {
  status: 'online' | 'offline' | 'busy' | 'away' | 'active' | 'inactive' | 'pending' | 'approved' | 'rejected';
}

export const StatusBadge = forwardRef<HTMLSpanElement, StatusBadgeProps>(({
  status,
  ...props
}, ref) => {
  const statusConfig = {
    online: { variant: 'success' as const, label: 'Online', dot: true },
    offline: { variant: 'default' as const, label: 'Offline', dot: true },
    busy: { variant: 'danger' as const, label: 'Busy', dot: true },
    away: { variant: 'warning' as const, label: 'Away', dot: true },
    active: { variant: 'success' as const, label: 'Active' },
    inactive: { variant: 'default' as const, label: 'Inactive' },
    pending: { variant: 'warning' as const, label: 'Pending' },
    approved: { variant: 'success' as const, label: 'Approved' },
    rejected: { variant: 'danger' as const, label: 'Rejected' },
  };

  const config = statusConfig[status];

  return (
    <Badge
      ref={ref}
      variant={config.variant}
      dot={config.dot}
      {...props}
    >
      {!config.dot && config.label}
    </Badge>
  );
});

StatusBadge.displayName = 'StatusBadge';
