// AIFOLIO Elite System - Static InlineNote Atom
// NO-SENTIENCE SHIELD: Read-only muted or warning text, zero logic risk
// LOCKDOWN MODE: No state, no hooks, no dynamic behavior

import React from 'react';

// Immutable prop schema - NO MUTATIONS ALLOWED
interface InlineNoteProps {
  readonly children: React.ReactNode;
  readonly variant?: 'muted' | 'info' | 'success' | 'warning' | 'danger';
  readonly size?: 'xs' | 'sm' | 'md';
  readonly icon?: React.ReactNode;
  readonly className?: string;
}

// STATIC COMPONENT - CRYSTALLIZED RENDER ONLY
export const InlineNote: React.FC<InlineNoteProps> = ({
  children,
  variant = 'muted',
  size = 'sm',
  icon,
  className = ''
}) => {
  // LOCKDOWN: Pre-computed static styles only
  const variantClasses = {
    muted: 'text-gray-500 dark:text-gray-400',
    info: 'text-blue-600 dark:text-blue-400',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-500',
    danger: 'text-red-600 dark:text-red-400'
  } as const;

  const sizeClasses = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-base'
  } as const;

  const iconSizeClasses = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5'
  } as const;

  // IMMUTABLE CLASS COMPOSITION
  const noteClasses = [
    'inline-flex items-start gap-1.5',
    'leading-relaxed',
    variantClasses[variant],
    sizeClasses[size],
    className
  ].filter(Boolean).join(' ');

  const iconClasses = [
    iconSizeClasses[size],
    'flex-shrink-0 mt-0.5'
  ].join(' ');

  // STATIC RENDER - NO LOGIC, NO STATE, NO SENTIENCE
  return (
    <span
      className={noteClasses}
      data-lockdown-component="InlineNote"
      data-no-sentience="enforced"
      data-variant={variant}
      data-size={size}
      role={variant === 'warning' || variant === 'danger' ? 'alert' : undefined}
    >
      {icon && (
        <span className={iconClasses} aria-hidden="true">
          {icon}
        </span>
      )}

      <span className="min-w-0">
        {children}
      </span>
    </span>
  );
};

// LOCKDOWN METADATA
InlineNote.displayName = 'InlineNote';

// SCHEMA VALIDATION - RUNTIME GUARD
if (process.env.NODE_ENV === 'development') {
  const originalInlineNote = InlineNote;

  // @ts-ignore - Development-only override
  InlineNote = (props: InlineNoteProps) => {
    // Validate prop schema at runtime
    const allowedProps = ['children', 'variant', 'size', 'icon', 'className'];
    const propKeys = Object.keys(props);

    for (const key of propKeys) {
      if (!allowedProps.includes(key)) {
        console.error(`🚨 LOCKDOWN VIOLATION: Unauthorized prop "${key}" in InlineNote component`);
        throw new Error(`NO-SENTIENCE SHIELD: Prop "${key}" not allowed in static component`);
      }
    }

    // Validate children is not a function (could contain logic)
    if (typeof props.children === 'function') {
      console.error('🚨 LOCKDOWN VIOLATION: Function children not allowed in static InlineNote');
      throw new Error('NO-SENTIENCE SHIELD: Function children could contain logic');
    }

    return originalInlineNote(props);
  };
}
