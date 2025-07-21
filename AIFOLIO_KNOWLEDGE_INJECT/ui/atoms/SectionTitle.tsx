// AIFOLIO Elite System - Static SectionTitle Atom
// NO-SENTIENCE SHIELD: Read-only H2/H3 text blocks, zero logic risk
// LOCKDOWN MODE: No state, no hooks, no dynamic behavior

import React from 'react';

// Immutable prop schema - NO MUTATIONS ALLOWED
interface SectionTitleProps {
  readonly children: React.ReactNode;
  readonly level?: 2 | 3 | 4 | 5 | 6;
  readonly size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  readonly weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  readonly color?: 'default' | 'muted' | 'accent' | 'success' | 'warning' | 'danger';
  readonly className?: string;
}

// STATIC COMPONENT - CRYSTALLIZED RENDER ONLY
export const SectionTitle: React.FC<SectionTitleProps> = ({
  children,
  level = 2,
  size = 'lg',
  weight = 'semibold',
  color = 'default',
  className = ''
}) => {
  // LOCKDOWN: Pre-computed static styles only
  const sizeClasses = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl'
  } as const;

  const weightClasses = {
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
    bold: 'font-bold'
  } as const;

  const colorClasses = {
    default: 'text-gray-900 dark:text-gray-100',
    muted: 'text-gray-600 dark:text-gray-400',
    accent: 'text-blue-600 dark:text-blue-400',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    danger: 'text-red-600 dark:text-red-400'
  } as const;

  // IMMUTABLE CLASS COMPOSITION
  const titleClasses = [
    'leading-tight tracking-tight',
    sizeClasses[size],
    weightClasses[weight],
    colorClasses[color],
    className
  ].filter(Boolean).join(' ');

  // STATIC HEADING ELEMENTS - NO LOGIC, NO STATE, NO SENTIENCE
  const headingProps = {
    className: titleClasses,
    'data-lockdown-component': 'SectionTitle',
    'data-no-sentience': 'enforced',
    'data-level': level,
    'data-size': size
  };

  // IMMUTABLE HEADING RENDER BASED ON LEVEL
  switch (level) {
    case 2:
      return <h2 {...headingProps}>{children}</h2>;
    case 3:
      return <h3 {...headingProps}>{children}</h3>;
    case 4:
      return <h4 {...headingProps}>{children}</h4>;
    case 5:
      return <h5 {...headingProps}>{children}</h5>;
    case 6:
      return <h6 {...headingProps}>{children}</h6>;
    default:
      return <h2 {...headingProps}>{children}</h2>;
  }
};

// LOCKDOWN METADATA
SectionTitle.displayName = 'SectionTitle';

// SCHEMA VALIDATION - RUNTIME GUARD
if (process.env.NODE_ENV === 'development') {
  const originalSectionTitle = SectionTitle;
  
  // @ts-ignore - Development-only override
  SectionTitle = (props: SectionTitleProps) => {
    // Validate prop schema at runtime
    const allowedProps = ['children', 'level', 'size', 'weight', 'color', 'className'];
    const propKeys = Object.keys(props);
    
    for (const key of propKeys) {
      if (!allowedProps.includes(key)) {
        console.error(`🚨 LOCKDOWN VIOLATION: Unauthorized prop "${key}" in SectionTitle component`);
        throw new Error(`NO-SENTIENCE SHIELD: Prop "${key}" not allowed in static component`);
      }
    }
    
    // Validate level is within allowed range
    if (props.level && (props.level < 2 || props.level > 6)) {
      console.error('🚨 LOCKDOWN VIOLATION: Invalid heading level in SectionTitle');
      throw new Error('NO-SENTIENCE SHIELD: Heading level must be between 2-6');
    }
    
    // Validate children is not a function (could contain logic)
    if (typeof props.children === 'function') {
      console.error('🚨 LOCKDOWN VIOLATION: Function children not allowed in static SectionTitle');
      throw new Error('NO-SENTIENCE SHIELD: Function children could contain logic');
    }
    
    return originalSectionTitle(props);
  };
}
