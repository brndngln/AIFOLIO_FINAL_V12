// AIFOLIO Elite System - Static Tag Atom
// NO-SENTIENCE SHIELD: Read-only label with optional icon, zero logic risk
// LOCKDOWN MODE: No state, no hooks, no dynamic behavior

import React from 'react';

// Immutable prop schema - NO MUTATIONS ALLOWED
interface TagProps {
  readonly children: React.ReactNode;
  readonly variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
  readonly size?: 'xs' | 'sm' | 'md' | 'lg';
  readonly icon?: React.ReactNode;
  readonly iconPosition?: 'left' | 'right';
  readonly className?: string;
}

// STATIC COMPONENT - CRYSTALLIZED RENDER ONLY
export const Tag: React.FC<TagProps> = ({
  children,
  variant = 'default',
  size = 'md',
  icon,
  iconPosition = 'left',
  className = ''
}) => {
  // LOCKDOWN: Pre-computed static styles only
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
    primary: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    secondary: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  } as const;

  const sizeClasses = {
    xs: 'px-2 py-0.5 text-xs',
    sm: 'px-2.5 py-0.5 text-sm',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base'
  } as const;

  const iconSizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  } as const;

  // IMMUTABLE CLASS COMPOSITION
  const tagClasses = [
    'inline-flex items-center gap-1.5 rounded-full font-medium',
    'transition-none', // NO ANIMATIONS - STATIC ONLY
    variantClasses[variant],
    sizeClasses[size],
    className
  ].filter(Boolean).join(' ');

  const iconClasses = [
    iconSizeClasses[size],
    'flex-shrink-0'
  ].join(' ');

  // STATIC RENDER - NO LOGIC, NO STATE, NO SENTIENCE
  return (
    <span 
      className={tagClasses}
      data-lockdown-component="Tag"
      data-no-sentience="enforced"
      data-variant={variant}
      data-size={size}
    >
      {icon && iconPosition === 'left' && (
        <span className={iconClasses} aria-hidden="true">
          {icon}
        </span>
      )}
      
      <span className="truncate">
        {children}
      </span>
      
      {icon && iconPosition === 'right' && (
        <span className={iconClasses} aria-hidden="true">
          {icon}
        </span>
      )}
    </span>
  );
};

// LOCKDOWN METADATA
Tag.displayName = 'Tag';

// SCHEMA VALIDATION - RUNTIME GUARD
if (process.env.NODE_ENV === 'development') {
  const originalTag = Tag;
  
  // @ts-ignore - Development-only override
  Tag = (props: TagProps) => {
    // Validate prop schema at runtime
    const allowedProps = ['children', 'variant', 'size', 'icon', 'iconPosition', 'className'];
    const propKeys = Object.keys(props);
    
    for (const key of propKeys) {
      if (!allowedProps.includes(key)) {
        console.error(`🚨 LOCKDOWN VIOLATION: Unauthorized prop "${key}" in Tag component`);
        throw new Error(`NO-SENTIENCE SHIELD: Prop "${key}" not allowed in static component`);
      }
    }
    
    // Validate children is not a function (could contain logic)
    if (typeof props.children === 'function') {
      console.error('🚨 LOCKDOWN VIOLATION: Function children not allowed in static Tag');
      throw new Error('NO-SENTIENCE SHIELD: Function children could contain logic');
    }
    
    return originalTag(props);
  };
}
