// AIFOLIO Elite System - Static TooltipHint Atom
// NO-SENTIENCE SHIELD: Read-only hover tips with NO event listeners, zero logic risk
// LOCKDOWN MODE: No state, no hooks, no dynamic behavior, CSS-only hover

import React from 'react';

// Immutable prop schema - NO MUTATIONS ALLOWED
interface TooltipHintProps {
  readonly children: React.ReactNode;
  readonly hint: string;
  readonly position?: 'top' | 'bottom' | 'left' | 'right';
  readonly size?: 'sm' | 'md' | 'lg';
  readonly className?: string;
}

// STATIC COMPONENT - CRYSTALLIZED RENDER ONLY
export const TooltipHint: React.FC<TooltipHintProps> = ({
  children,
  hint,
  position = 'top',
  size = 'md',
  className = ''
}) => {
  // LOCKDOWN: Pre-computed static styles only - CSS HOVER ONLY
  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  } as const;

  const arrowClasses = {
    top: 'top-full left-1/2 transform -translate-x-1/2 border-t-gray-900 border-t-4 border-x-transparent border-x-4 border-b-0',
    bottom: 'bottom-full left-1/2 transform -translate-x-1/2 border-b-gray-900 border-b-4 border-x-transparent border-x-4 border-t-0',
    left: 'left-full top-1/2 transform -translate-y-1/2 border-l-gray-900 border-l-4 border-y-transparent border-y-4 border-r-0',
    right: 'right-full top-1/2 transform -translate-y-1/2 border-r-gray-900 border-r-4 border-y-transparent border-y-4 border-l-0'
  } as const;

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs max-w-32',
    md: 'px-3 py-1.5 text-sm max-w-48',
    lg: 'px-4 py-2 text-base max-w-64'
  } as const;

  // IMMUTABLE CLASS COMPOSITION
  const wrapperClasses = [
    'relative inline-block group',
    className
  ].filter(Boolean).join(' ');

  const tooltipClasses = [
    'absolute z-50 pointer-events-none',
    'opacity-0 group-hover:opacity-100',
    'transition-opacity duration-200',
    'bg-gray-900 text-white rounded-md shadow-lg',
    'whitespace-nowrap',
    positionClasses[position],
    sizeClasses[size]
  ].join(' ');

  const arrowElementClasses = [
    'absolute w-0 h-0',
    arrowClasses[position]
  ].join(' ');

  // STATIC RENDER - NO LOGIC, NO STATE, NO SENTIENCE
  // CSS-ONLY HOVER - NO EVENT LISTENERS
  return (
    <div 
      className={wrapperClasses}
      data-lockdown-component="TooltipHint"
      data-no-sentience="enforced"
      data-position={position}
    >
      {children}
      
      {/* CSS-ONLY TOOLTIP - NO JAVASCRIPT */}
      <div className={tooltipClasses}>
        <div className="relative">
          {hint}
          <div className={arrowElementClasses} />
        </div>
      </div>
    </div>
  );
};

// LOCKDOWN METADATA
TooltipHint.displayName = 'TooltipHint';

// SCHEMA VALIDATION - RUNTIME GUARD
if (process.env.NODE_ENV === 'development') {
  const originalTooltipHint = TooltipHint;
  
  // @ts-ignore - Development-only override
  TooltipHint = (props: TooltipHintProps) => {
    // Validate prop schema at runtime
    const allowedProps = ['children', 'hint', 'position', 'size', 'className'];
    const propKeys = Object.keys(props);
    
    for (const key of propKeys) {
      if (!allowedProps.includes(key)) {
        console.error(`🚨 LOCKDOWN VIOLATION: Unauthorized prop "${key}" in TooltipHint component`);
        throw new Error(`NO-SENTIENCE SHIELD: Prop "${key}" not allowed in static component`);
      }
    }
    
    // Validate children is not a function (could contain logic)
    if (typeof props.children === 'function') {
      console.error('🚨 LOCKDOWN VIOLATION: Function children not allowed in static TooltipHint');
      throw new Error('NO-SENTIENCE SHIELD: Function children could contain logic');
    }
    
    // Validate hint is a string (no dynamic content)
    if (typeof props.hint !== 'string') {
      console.error('🚨 LOCKDOWN VIOLATION: Hint must be static string in TooltipHint');
      throw new Error('NO-SENTIENCE SHIELD: Hint must be static string, no dynamic content');
    }
    
    return originalTooltipHint(props);
  };
}
