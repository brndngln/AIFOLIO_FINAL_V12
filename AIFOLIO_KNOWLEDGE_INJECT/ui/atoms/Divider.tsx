// AIFOLIO Elite System - Static Divider Atom
// NO-SENTIENCE SHIELD: Read-only visual separator with zero logic risk
// LOCKDOWN MODE: No state, no hooks, no dynamic behavior

import React from 'react';

// Immutable prop schema - NO MUTATIONS ALLOWED
interface DividerProps {
  readonly orientation?: 'horizontal' | 'vertical';
  readonly size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  readonly color?: 'light' | 'medium' | 'dark' | 'accent';
  readonly className?: string;
}

// STATIC COMPONENT - CRYSTALLIZED RENDER ONLY
export const Divider: React.FC<DividerProps> = ({
  orientation = 'horizontal',
  size = 'md',
  color = 'medium',
  className = ''
}) => {
  // LOCKDOWN: Pre-computed static styles only
  const orientationClasses = {
    horizontal: 'w-full h-px',
    vertical: 'h-full w-px'
  } as const;

  const sizeClasses = {
    xs: orientation === 'horizontal' ? 'h-px' : 'w-px',
    sm: orientation === 'horizontal' ? 'h-0.5' : 'w-0.5',
    md: orientation === 'horizontal' ? 'h-px' : 'w-px',
    lg: orientation === 'horizontal' ? 'h-0.5' : 'w-0.5',
    xl: orientation === 'horizontal' ? 'h-1' : 'w-1'
  } as const;

  const colorClasses = {
    light: 'bg-gray-200 dark:bg-gray-700',
    medium: 'bg-gray-300 dark:bg-gray-600',
    dark: 'bg-gray-400 dark:bg-gray-500',
    accent: 'bg-blue-500 dark:bg-blue-400'
  } as const;

  // IMMUTABLE CLASS COMPOSITION
  const dividerClasses = [
    orientationClasses[orientation],
    sizeClasses[size],
    colorClasses[color],
    'flex-shrink-0',
    className
  ].filter(Boolean).join(' ');

  // STATIC RENDER - NO LOGIC, NO STATE, NO SENTIENCE
  return (
    <div
      className={dividerClasses}
      role="separator"
      aria-orientation={orientation}
      data-lockdown-component="Divider"
      data-no-sentience="enforced"
    />
  );
};

// LOCKDOWN METADATA
Divider.displayName = 'Divider';

// SCHEMA VALIDATION - RUNTIME GUARD
if (process.env.NODE_ENV === 'development') {
  const originalDivider = Divider;

  // @ts-ignore - Development-only override
  Divider = (props: DividerProps) => {
    // Validate prop schema at runtime
    const allowedProps = ['orientation', 'size', 'color', 'className'];
    const propKeys = Object.keys(props);

    for (const key of propKeys) {
      if (!allowedProps.includes(key)) {
        console.error(`🚨 LOCKDOWN VIOLATION: Unauthorized prop "${key}" in Divider component`);
        throw new Error(`NO-SENTIENCE SHIELD: Prop "${key}" not allowed in static component`);
      }
    }

    return originalDivider(props);
  };
}
