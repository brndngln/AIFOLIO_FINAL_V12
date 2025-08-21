// AIFOLIO Elite System - LockdownGate Route & Component Validator
// NO-SENTIENCE SHIELD: Checks routes, components, props against safelist
// LOCKDOWN MODE: Blocks unauthorized components and validates prop schemas

import React, { useEffect, useState } from 'react';

// Immutable gate configuration - NO MUTATIONS ALLOWED
interface LockdownGateProps {
  readonly children: React.ReactNode;
  readonly allowedComponents?: readonly string[];
  readonly allowedRoutes?: readonly string[];
  readonly strictPropValidation?: boolean;
  readonly blockUnknownComponents?: boolean;
  readonly className?: string;
}

// Component registry for validation
const APPROVED_COMPONENTS = [
  'Divider',
  'Tag',
  'SectionTitle',
  'InlineNote',
  'TooltipHint',
  'Button',
  'AppWrapper',
  'RenderCage',
  'LockdownGate',
  'LockdownDebugger'
] as const;

// Route safelist
const APPROVED_ROUTES = [
  '/',
  '/vault',
  '/vault/:id',
  '/settings',
  '/debug'
] as const;

// Prop schema registry
const COMPONENT_PROP_SCHEMAS = {
  Divider: ['orientation', 'size', 'color', 'className'],
  Tag: ['children', 'variant', 'size', 'icon', 'iconPosition', 'className'],
  SectionTitle: ['children', 'level', 'size', 'weight', 'color', 'className'],
  InlineNote: ['children', 'variant', 'size', 'icon', 'className'],
  TooltipHint: ['children', 'hint', 'position', 'size', 'className']
} as const;

// LOCKDOWN GATE COMPONENT - COMPONENT & ROUTE VALIDATOR
export const LockdownGate: React.FC<LockdownGateProps> = ({
  children,
  allowedComponents = APPROVED_COMPONENTS,
  allowedRoutes = APPROVED_ROUTES,
  strictPropValidation = true,
  blockUnknownComponents = true,
  className = ''
}) => {
  const [gateStatus, setGateStatus] = useState<'CHECKING' | 'APPROVED' | 'BLOCKED'>('CHECKING');
  const [violations, setViolations] = useState<string[]>([]);
  const [currentRoute, setCurrentRoute] = useState<string>('');

  // ROUTE VALIDATION
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const path = window.location.pathname;
      setCurrentRoute(path);

      // Check if current route is approved
      const isRouteApproved = allowedRoutes.some(route => {
        // Handle parameterized routes
        const routePattern = route.replace(/:[\w]+/g, '[^/]+');
        const regex = new RegExp(`^${routePattern}$`);
        return regex.test(path);
      });

      if (!isRouteApproved) {
        const violation = `Unauthorized route: ${path}`;
        setViolations(prev => [...prev, violation]);
        reportViolation('ROGUE_RENDER', 'LockdownGate', violation);

        if (blockUnknownComponents) {
          setGateStatus('BLOCKED');
          return;
        }
      }
    }
  }, [allowedRoutes, blockUnknownComponents]);

  // COMPONENT TREE VALIDATION
  useEffect(() => {
    if (strictPropValidation) {
      validateComponentTree(children);
    }

    // If no violations and route is approved, allow render
    if (violations.length === 0) {
      setGateStatus('APPROVED');
    }
  }, [children, strictPropValidation, violations.length]);

  // COMPONENT TREE VALIDATOR
  const validateComponentTree = (node: React.ReactNode): void => {
    if (!node) return;

    if (React.isValidElement(node)) {
      const componentName = getComponentName(node);

      // Check if component is approved
      if (componentName && !allowedComponents.includes(componentName as any)) {
        const violation = `Unauthorized component: ${componentName}`;
        setViolations(prev => [...prev, violation]);
        reportViolation('ROGUE_RENDER', 'LockdownGate', violation);

        if (blockUnknownComponents) {
          setGateStatus('BLOCKED');
          return;
        }
      }

      // Validate props if schema exists
      if (componentName && COMPONENT_PROP_SCHEMAS[componentName as keyof typeof COMPONENT_PROP_SCHEMAS]) {
        const allowedProps = COMPONENT_PROP_SCHEMAS[componentName as keyof typeof COMPONENT_PROP_SCHEMAS];
        const nodeProps = Object.keys(node.props || {});

        for (const prop of nodeProps) {
          if (!allowedProps.includes(prop as any) && prop !== 'children') {
            const violation = `Unauthorized prop "${prop}" in ${componentName}`;
            setViolations(prev => [...prev, violation]);
            reportViolation('UNAUTHORIZED_PROP', componentName, violation);
          }
        }
      }

      // Recursively validate children
      if (node.props && node.props.children) {
        React.Children.forEach(node.props.children, validateComponentTree);
      }
    } else if (Array.isArray(node)) {
      node.forEach(validateComponentTree);
    }
  };

  // COMPONENT NAME EXTRACTOR
  const getComponentName = (element: React.ReactElement): string | null => {
    if (element.type) {
      if (typeof element.type === 'string') {
        return element.type; // HTML elements
      } else if (typeof element.type === 'function') {
        return element.type.displayName || element.type.name || null;
      }
    }
    return null;
  };

  // VIOLATION REPORTER
  const reportViolation = (
    type: 'UNAUTHORIZED_PROP' | 'ROGUE_RENDER' | 'LOGIC_INJECTION' | 'STATE_MUTATION',
    component: string,
    details: string
  ) => {
    console.error(`🚨 LOCKDOWN GATE VIOLATION [${type}]:`, {
      component,
      details,
      route: currentRoute,
      timestamp: new Date().toISOString()
    });

    // Report to global violation system if available
    if (typeof window !== 'undefined' && window.__AIFOLIO_REPORT_VIOLATION__) {
      window.__AIFOLIO_REPORT_VIOLATION__(type, component, details);
    }
  };

  // GATE STATUS CLASSES
  const gateClasses = [
    'lockdown-gate',
    'relative',
    `gate-status-${gateStatus.toLowerCase()}`,
    className
  ].filter(Boolean).join(' ');

  // BLOCKED STATE RENDER
  if (gateStatus === 'BLOCKED') {
    return (
      <div
        className="lockdown-gate-blocked min-h-screen bg-red-950 text-red-100 flex items-center justify-center"
        data-lockdown-component="LockdownGate"
        data-gate-status="BLOCKED"
        data-violations={violations.length}
      >
        <div className="text-center max-w-md p-8">
          <div className="text-6xl mb-4">🚫</div>
          <h1 className="text-2xl font-bold mb-4">LOCKDOWN GATE: ACCESS DENIED</h1>
          <p className="text-red-300 mb-6">
            Unauthorized component or route detected. Render blocked by NO-SENTIENCE SHIELD.
          </p>

          {violations.length > 0 && (
            <div className="bg-red-900 p-4 rounded-lg text-left">
              <h2 className="font-semibold mb-2">Violations Detected:</h2>
              <ul className="text-sm space-y-1">
                {violations.map((violation, index) => (
                  <li key={index} className="text-red-200">• {violation}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-6 text-xs text-red-400">
            Route: {currentRoute} | Gate Status: {gateStatus}
          </div>
        </div>
      </div>
    );
  }

  // CHECKING STATE RENDER
  if (gateStatus === 'CHECKING') {
    return (
      <div
        className="lockdown-gate-checking min-h-screen bg-yellow-950 text-yellow-100 flex items-center justify-center"
        data-lockdown-component="LockdownGate"
        data-gate-status="CHECKING"
      >
        <div className="text-center">
          <div className="text-4xl mb-4">🔍</div>
          <p className="text-lg">LOCKDOWN GATE: Validating components...</p>
          <div className="mt-4 text-sm text-yellow-300">
            Route: {currentRoute}
          </div>
        </div>
      </div>
    );
  }

  // APPROVED STATE RENDER
  return (
    <div
      className={gateClasses}
      data-lockdown-component="LockdownGate"
      data-gate-status="APPROVED"
      data-route={currentRoute}
      data-violations={violations.length}
      data-no-sentience="enforced"
    >
      {/* GATE STATUS INDICATOR (DEV ONLY) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed top-16 right-4 z-[9999] bg-green-900 text-green-100 px-3 py-2 rounded-lg shadow-lg text-xs font-mono">
          🚪 GATE: {gateStatus} | Route: {currentRoute}
        </div>
      )}

      {/* APPROVED CHILDREN RENDER */}
      {children}
    </div>
  );
};

// LOCKDOWN METADATA
LockdownGate.displayName = 'LockdownGate';
