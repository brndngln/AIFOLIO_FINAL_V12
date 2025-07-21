// AIFOLIO Elite System - LockdownDebugger Developer HUD
// NO-SENTIENCE SHIELD: Dev-only HUD to confirm render activity and violations
// LOCKDOWN MODE: Real-time monitoring and anomaly detection display

import React, { useEffect, useState, useCallback } from 'react';

// Immutable debugger configuration - NO MUTATIONS ALLOWED
interface LockdownDebuggerProps {
  readonly enabled?: boolean;
  readonly position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  readonly minimized?: boolean;
  readonly showViolations?: boolean;
  readonly showPerformance?: boolean;
  readonly className?: string;
}

// Debug metrics interface
interface DebugMetrics {
  readonly renderCount: number;
  readonly violationCount: number;
  readonly lastRender: number;
  readonly averageRenderTime: number;
  readonly memoryUsage?: number;
  readonly componentCount: number;
}

// Violation history interface
interface ViolationHistory {
  readonly id: string;
  readonly timestamp: number;
  readonly type: string;
  readonly component: string;
  readonly details: string;
}

// LOCKDOWN DEBUGGER COMPONENT - DEV-ONLY HUD
export const LockdownDebugger: React.FC<LockdownDebuggerProps> = ({
  enabled = process.env.NODE_ENV === 'development',
  position = 'bottom-left',
  minimized = false,
  showViolations = true,
  showPerformance = true,
  className = ''
}) => {
  const [isMinimized, setIsMinimized] = useState(minimized);
  const [metrics, setMetrics] = useState<DebugMetrics>({
    renderCount: 0,
    violationCount: 0,
    lastRender: Date.now(),
    averageRenderTime: 0,
    componentCount: 0
  });
  const [violations, setViolations] = useState<ViolationHistory[]>([]);
  const [isLockdownActive, setIsLockdownActive] = useState(true);

  // METRICS COLLECTION
  useEffect(() => {
    if (!enabled) return;

    let renderStartTime = performance.now();
    let renderTimes: number[] = [];

    // Monitor render performance
    const updateMetrics = () => {
      const renderEndTime = performance.now();
      const renderTime = renderEndTime - renderStartTime;
      renderTimes.push(renderTime);
      
      // Keep only last 100 render times
      if (renderTimes.length > 100) {
        renderTimes = renderTimes.slice(-100);
      }

      const averageRenderTime = renderTimes.reduce((a, b) => a + b, 0) / renderTimes.length;

      setMetrics(prev => ({
        ...prev,
        renderCount: prev.renderCount + 1,
        lastRender: Date.now(),
        averageRenderTime,
        memoryUsage: (performance as any).memory?.usedJSHeapSize || 0,
        componentCount: document.querySelectorAll('[data-lockdown-component]').length
      }));

      renderStartTime = performance.now();
    };

    // Monitor violations from localStorage
    const checkViolations = () => {
      try {
        const storedViolations = JSON.parse(
          localStorage.getItem('aifolio_lockdown_violations') || '[]'
        );
        
        const formattedViolations: ViolationHistory[] = storedViolations.map((v: any) => ({
          id: v.id,
          timestamp: v.timestamp,
          type: v.type,
          component: v.component,
          details: v.details
        }));

        setViolations(formattedViolations.slice(-20)); // Keep last 20
        setMetrics(prev => ({
          ...prev,
          violationCount: formattedViolations.length
        }));
      } catch (error) {
        console.warn('Failed to load violation history:', error);
      }
    };

    // Check lockdown status
    const checkLockdownStatus = () => {
      const lockdownActive = typeof window !== 'undefined' && 
        window.__AIFOLIO_NO_SENTIENCE__ === 'ENFORCED';
      setIsLockdownActive(lockdownActive);
    };

    // Initial checks
    updateMetrics();
    checkViolations();
    checkLockdownStatus();

    // Set up intervals
    const metricsInterval = setInterval(updateMetrics, 1000);
    const violationsInterval = setInterval(checkViolations, 2000);
    const statusInterval = setInterval(checkLockdownStatus, 5000);

    return () => {
      clearInterval(metricsInterval);
      clearInterval(violationsInterval);
      clearInterval(statusInterval);
    };
  }, [enabled]);

  // CLEAR VIOLATIONS
  const clearViolations = useCallback(() => {
    localStorage.removeItem('aifolio_lockdown_violations');
    setViolations([]);
    setMetrics(prev => ({ ...prev, violationCount: 0 }));
  }, []);

  // TOGGLE MINIMIZED STATE
  const toggleMinimized = useCallback(() => {
    setIsMinimized(prev => !prev);
  }, []);

  // Don't render if disabled or in production
  if (!enabled || process.env.NODE_ENV === 'production') {
    return null;
  }

  // POSITION CLASSES
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  // DEBUGGER CLASSES
  const debuggerClasses = [
    'fixed z-[10000] bg-gray-900 text-gray-100 rounded-lg shadow-2xl border border-gray-700',
    'font-mono text-xs',
    'transition-all duration-300',
    isMinimized ? 'w-48' : 'w-80',
    positionClasses[position],
    className
  ].filter(Boolean).join(' ');

  // STATUS COLORS
  const getStatusColor = (status: boolean) => status ? 'text-green-400' : 'text-red-400';
  const getViolationColor = (count: number) => {
    if (count === 0) return 'text-green-400';
    if (count < 5) return 'text-yellow-400';
    return 'text-red-400';
  };

  // DEBUGGER RENDER
  return (
    <div 
      className={debuggerClasses}
      data-lockdown-component="LockdownDebugger"
      data-no-sentience="enforced"
      data-minimized={isMinimized}
    >
      {/* DEBUGGER HEADER */}
      <div className="flex items-center justify-between p-3 border-b border-gray-700">
        <div className="flex items-center gap-2">
          <span className="text-blue-400">🛡️</span>
          <span className="font-semibold">LOCKDOWN DEBUG</span>
        </div>
        <button
          onClick={toggleMinimized}
          className="text-gray-400 hover:text-gray-200 transition-colors"
          aria-label={isMinimized ? 'Expand debugger' : 'Minimize debugger'}
        >
          {isMinimized ? '📈' : '📉'}
        </button>
      </div>

      {/* MINIMIZED VIEW */}
      {isMinimized ? (
        <div className="p-3 space-y-2">
          <div className="flex justify-between">
            <span>Status:</span>
            <span className={getStatusColor(isLockdownActive)}>
              {isLockdownActive ? 'ACTIVE' : 'DISABLED'}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Violations:</span>
            <span className={getViolationColor(metrics.violationCount)}>
              {metrics.violationCount}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Components:</span>
            <span className="text-blue-400">{metrics.componentCount}</span>
          </div>
        </div>
      ) : (
        /* EXPANDED VIEW */
        <div className="p-3 space-y-4">
          {/* LOCKDOWN STATUS */}
          <div className="space-y-2">
            <h3 className="text-blue-400 font-semibold">System Status</h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>Lockdown: <span className={getStatusColor(isLockdownActive)}>
                {isLockdownActive ? 'ACTIVE' : 'DISABLED'}
              </span></div>
              <div>Components: <span className="text-blue-400">{metrics.componentCount}</span></div>
              <div>Renders: <span className="text-green-400">{metrics.renderCount}</span></div>
              <div>Avg Render: <span className="text-yellow-400">
                {metrics.averageRenderTime.toFixed(2)}ms
              </span></div>
            </div>
          </div>

          {/* PERFORMANCE METRICS */}
          {showPerformance && (
            <div className="space-y-2">
              <h3 className="text-green-400 font-semibold">Performance</h3>
              <div className="text-xs space-y-1">
                <div>Memory: <span className="text-yellow-400">
                  {metrics.memoryUsage ? `${(metrics.memoryUsage / 1024 / 1024).toFixed(1)}MB` : 'N/A'}
                </span></div>
                <div>Last Render: <span className="text-blue-400">
                  {new Date(metrics.lastRender).toLocaleTimeString()}
                </span></div>
              </div>
            </div>
          )}

          {/* VIOLATIONS */}
          {showViolations && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="text-red-400 font-semibold">
                  Violations ({metrics.violationCount})
                </h3>
                {violations.length > 0 && (
                  <button
                    onClick={clearViolations}
                    className="text-xs text-gray-400 hover:text-gray-200"
                  >
                    Clear
                  </button>
                )}
              </div>
              
              {violations.length === 0 ? (
                <div className="text-green-400 text-xs">✅ No violations detected</div>
              ) : (
                <div className="max-h-32 overflow-y-auto space-y-1">
                  {violations.slice(-5).map(violation => (
                    <div key={violation.id} className="text-xs bg-red-900/30 p-2 rounded">
                      <div className="text-red-300">[{violation.type}] {violation.component}</div>
                      <div className="text-red-400 truncate">{violation.details}</div>
                      <div className="text-gray-500">
                        {new Date(violation.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* CONTROLS */}
          <div className="pt-2 border-t border-gray-700">
            <div className="flex gap-2 text-xs">
              <button
                onClick={() => console.log('AIFOLIO Lockdown Metrics:', metrics)}
                className="text-blue-400 hover:text-blue-300"
              >
                Log Metrics
              </button>
              <button
                onClick={() => console.log('AIFOLIO Violations:', violations)}
                className="text-yellow-400 hover:text-yellow-300"
              >
                Log Violations
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// LOCKDOWN METADATA
LockdownDebugger.displayName = 'LockdownDebugger';
