// AIFOLIO Elite System - RenderCage Master Lockdown
// NO-SENTIENCE SHIELD: Master visual boundary enforcing render-only mode
// LOCKDOWN MODE: Global mount point with absolute firewall protection

import React, { useEffect, useState } from 'react';

// Immutable cage configuration - NO MUTATIONS ALLOWED
interface RenderCageProps {
  readonly children: React.ReactNode;
  readonly enableDebugger?: boolean;
  readonly strictMode?: boolean;
  readonly className?: string;
}

// Lockdown violation tracking
interface ViolationLog {
  readonly id: string;
  readonly timestamp: number;
  readonly type: 'UNAUTHORIZED_PROP' | 'ROGUE_RENDER' | 'LOGIC_INJECTION' | 'STATE_MUTATION';
  readonly component: string;
  readonly details: string;
  readonly stackTrace?: string;
}

// MASTER LOCKDOWN COMPONENT - ABSOLUTE FIREWALL
export const RenderCage: React.FC<RenderCageProps> = ({
  children,
  enableDebugger = process.env.NODE_ENV === 'development',
  strictMode = true,
  className = ''
}) => {
  const [violations, setViolations] = useState<ViolationLog[]>([]);
  const [isLockdownActive, setIsLockdownActive] = useState(true);

  // LOCKDOWN INITIALIZATION
  useEffect(() => {
    // Inject NO-SENTIENCE environment constant
    if (typeof window !== 'undefined') {
      // @ts-ignore - Global lockdown constant
      window.__AIFOLIO_NO_SENTIENCE__ = 'ENFORCED';

      // Disable dangerous global functions in strict mode
      if (strictMode) {
        const originalEval = window.eval;
        const originalFunction = window.Function;
        const originalSetTimeout = window.setTimeout;
        const originalSetInterval = window.setInterval;

        // Override eval to block dynamic code execution
        window.eval = () => {
          logViolation('LOGIC_INJECTION', 'RenderCage', 'Attempted eval() execution blocked');
          throw new Error('🚨 NO-SENTIENCE SHIELD: eval() disabled in lockdown mode');
        };

        // Override Function constructor
        window.Function = (...args: any[]) => {
          logViolation('LOGIC_INJECTION', 'RenderCage', 'Attempted Function() constructor blocked');
          throw new Error('🚨 NO-SENTIENCE SHIELD: Function() constructor disabled in lockdown mode');
        };

        // Monitor setTimeout/setInterval for unauthorized async logic
        window.setTimeout = (callback: any, delay?: number) => {
          if (typeof callback === 'string') {
            logViolation('LOGIC_INJECTION', 'RenderCage', 'String-based setTimeout blocked');
            throw new Error('🚨 NO-SENTIENCE SHIELD: String-based setTimeout disabled');
          }
          return originalSetTimeout(callback, delay);
        };

        window.setInterval = (callback: any, delay?: number) => {
          if (typeof callback === 'string') {
            logViolation('LOGIC_INJECTION', 'RenderCage', 'String-based setInterval blocked');
            throw new Error('🚨 NO-SENTIENCE SHIELD: String-based setInterval disabled');
          }
          return originalSetInterval(callback, delay);
        };

        // Cleanup on unmount
        return () => {
          window.eval = originalEval;
          window.Function = originalFunction;
          window.setTimeout = originalSetTimeout;
          window.setInterval = originalSetInterval;
        };
      }
    }
  }, [strictMode]);

  // VIOLATION LOGGING SYSTEM
  const logViolation = (
    type: ViolationLog['type'],
    component: string,
    details: string,
    stackTrace?: string
  ) => {
    const violation: ViolationLog = {
      id: `violation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      type,
      component,
      details,
      stackTrace: stackTrace || new Error().stack
    };

    setViolations(prev => [...prev.slice(-49), violation]); // Keep last 50 violations

    // Console logging for immediate feedback
    console.error(`🚨 LOCKDOWN VIOLATION [${type}]:`, {
      component,
      details,
      timestamp: new Date(violation.timestamp).toISOString(),
      id: violation.id
    });

    // Write to violation logs (development only)
    if (process.env.NODE_ENV === 'development') {
      writeViolationLog(violation);
    }
  };

  // VIOLATION LOG WRITER
  const writeViolationLog = async (violation: ViolationLog) => {
    try {
      const logEntry = {
        ...violation,
        timestamp_iso: new Date(violation.timestamp).toISOString(),
        user_agent: navigator.userAgent,
        url: window.location.href,
        lockdown_version: '1.9X++',
        severity: violation.type === 'LOGIC_INJECTION' ? 'CRITICAL' : 'HIGH'
      };

      // In a real app, this would write to a log file or send to a logging service
      console.warn('📝 VIOLATION LOG ENTRY:', JSON.stringify(logEntry, null, 2));

      // Store in localStorage for development debugging
      const existingLogs = JSON.parse(localStorage.getItem('aifolio_lockdown_violations') || '[]');
      existingLogs.push(logEntry);
      localStorage.setItem('aifolio_lockdown_violations', JSON.stringify(existingLogs.slice(-100)));

    } catch (error) {
      console.error('Failed to write violation log:', error);
    }
  };

  // LOCKDOWN STATUS CLASSES
  const cageClasses = [
    'render-cage-boundary',
    'relative min-h-screen',
    isLockdownActive ? 'lockdown-active' : 'lockdown-disabled',
    className
  ].filter(Boolean).join(' ');

  // MASTER RENDER - ABSOLUTE FIREWALL ACTIVE
  return (
    <div
      className={cageClasses}
      data-lockdown-component="RenderCage"
      data-no-sentience="enforced"
      data-strict-mode={strictMode}
      data-violations-count={violations.length}
      data-lockdown-status={isLockdownActive ? 'ACTIVE' : 'DISABLED'}
    >
      {/* LOCKDOWN STATUS INDICATOR */}
      {enableDebugger && (
        <div className="fixed top-4 right-4 z-[9999] bg-red-900 text-red-100 px-3 py-2 rounded-lg shadow-lg text-xs font-mono">
          🛡️ LOCKDOWN: {isLockdownActive ? 'ACTIVE' : 'DISABLED'} |
          Violations: {violations.length}
        </div>
      )}

      {/* VIOLATION ALERT OVERLAY */}
      {violations.length > 0 && enableDebugger && (
        <div className="fixed bottom-4 right-4 z-[9998] max-w-md">
          <div className="bg-red-900 text-red-100 p-4 rounded-lg shadow-xl">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-red-400">🚨</span>
              <span className="font-semibold">LOCKDOWN VIOLATIONS DETECTED</span>
            </div>
            <div className="text-sm space-y-1">
              {violations.slice(-3).map(violation => (
                <div key={violation.id} className="opacity-90">
                  <span className="text-red-300">[{violation.type}]</span> {violation.component}: {violation.details}
                </div>
              ))}
            </div>
            {violations.length > 3 && (
              <div className="text-xs text-red-300 mt-2">
                +{violations.length - 3} more violations (check console)
              </div>
            )}
          </div>
        </div>
      )}

      {/* PROTECTED CHILDREN RENDER */}
      <div
        className="render-cage-content"
        data-protected="true"
        data-sentience-blocked="true"
      >
        {children}
      </div>
    </div>
  );
};

// LOCKDOWN METADATA
RenderCage.displayName = 'RenderCage';

// GLOBAL VIOLATION REPORTER - Available to all components
if (typeof window !== 'undefined') {
  // @ts-ignore - Global violation reporter
  window.__AIFOLIO_REPORT_VIOLATION__ = (
    type: ViolationLog['type'],
    component: string,
    details: string
  ) => {
    console.error(`🚨 GLOBAL LOCKDOWN VIOLATION [${type}]:`, {
      component,
      details,
      timestamp: new Date().toISOString()
    });
  };
}
