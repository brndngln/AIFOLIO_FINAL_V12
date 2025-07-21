// AIFOLIO Elite System - Anomaly Watchdog
// NO-SENTIENCE SHIELD: Track unauthorized UI behaviors with detailed metadata
// LOCKDOWN MODE: Log violations, prop mutations, and rogue renders

// Violation log entry interface
interface ViolationLogEntry {
  readonly id: string;
  readonly timestamp: number;
  readonly timestampISO: string;
  readonly type: 'UNAUTHORIZED_PROP' | 'ROGUE_RENDER' | 'UI_MUTATION' | 'LOGIC_INJECTION' | 'SCHEMA_VIOLATION';
  readonly severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  readonly component: string;
  readonly details: string;
  readonly stackTrace?: string;
  readonly metadata: {
    readonly userAgent: string;
    readonly url: string;
    readonly lockdownVersion: string;
    readonly routeContext?: string;
    readonly propKeys?: string[];
    readonly expectedProps?: string[];
    readonly violatingValue?: any;
  };
  readonly suggestedCorrection?: string;
}

// Anomaly detection metrics
interface AnomalyMetrics {
  readonly totalViolations: number;
  readonly violationsByType: Record<string, number>;
  readonly violationsByComponent: Record<string, number>;
  readonly lastViolationTime: number;
  readonly averageViolationsPerHour: number;
  readonly criticalViolations: number;
}

// ANOMALY WATCHDOG CLASS - VIOLATION TRACKING & LOGGING
export class AnomalyWatchdog {
  private static instance: AnomalyWatchdog | null = null;
  private violations: ViolationLogEntry[] = [];
  private readonly maxViolations = 1000;
  private readonly storageKey = 'aifolio_anomaly_violations';

  // SINGLETON PATTERN - ENSURE SINGLE WATCHDOG INSTANCE
  static getInstance(): AnomalyWatchdog {
    if (!AnomalyWatchdog.instance) {
      AnomalyWatchdog.instance = new AnomalyWatchdog();
    }
    return AnomalyWatchdog.instance;
  }

  private constructor() {
    this.loadViolationsFromStorage();
    this.setupGlobalErrorHandlers();
    this.startPeriodicCleanup();
  }

  // LOG VIOLATION WITH FULL METADATA
  logViolation(
    type: ViolationLogEntry['type'],
    component: string,
    details: string,
    options: {
      severity?: ViolationLogEntry['severity'];
      stackTrace?: string;
      routeContext?: string;
      propKeys?: string[];
      expectedProps?: string[];
      violatingValue?: any;
      suggestedCorrection?: string;
    } = {}
  ): void {
    const violation: ViolationLogEntry = {
      id: this.generateViolationId(),
      timestamp: Date.now(),
      timestampISO: new Date().toISOString(),
      type,
      severity: options.severity || this.determineSeverity(type),
      component,
      details,
      stackTrace: options.stackTrace || new Error().stack,
      metadata: {
        userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'Unknown',
        url: typeof window !== 'undefined' ? window.location.href : 'Unknown',
        lockdownVersion: '1.9X++',
        routeContext: options.routeContext || this.getCurrentRoute(),
        propKeys: options.propKeys,
        expectedProps: options.expectedProps,
        violatingValue: this.sanitizeValue(options.violatingValue)
      },
      suggestedCorrection: options.suggestedCorrection || this.generateSuggestion(type, component)
    };

    // Add to violations array
    this.violations.push(violation);
    
    // Maintain max violations limit
    if (this.violations.length > this.maxViolations) {
      this.violations = this.violations.slice(-this.maxViolations);
    }

    // Persist to storage
    this.saveViolationsToStorage();

    // Console logging with color coding
    this.logToConsole(violation);

    // Trigger alerts for critical violations
    if (violation.severity === 'CRITICAL') {
      this.triggerCriticalAlert(violation);
    }
  }

  // LOG UNAUTHORIZED PROP INJECTION
  logUnauthorizedProp(
    component: string,
    propKey: string,
    expectedProps: string[],
    violatingValue?: any
  ): void {
    this.logViolation(
      'UNAUTHORIZED_PROP',
      component,
      `Unauthorized prop "${propKey}" detected`,
      {
        severity: 'HIGH',
        propKeys: [propKey],
        expectedProps,
        violatingValue,
        suggestedCorrection: `Remove prop "${propKey}" or add it to the approved schema for ${component}`
      }
    );
  }

  // LOG ROGUE COMPONENT RENDER
  logRogueRender(
    component: string,
    routeContext: string,
    details: string
  ): void {
    this.logViolation(
      'ROGUE_RENDER',
      component,
      `Unauthorized component render: ${details}`,
      {
        severity: 'CRITICAL',
        routeContext,
        suggestedCorrection: `Add "${component}" to the approved component registry or remove from render tree`
      }
    );
  }

  // LOG UI MUTATION ATTEMPT
  logUIMutation(
    component: string,
    mutationType: string,
    details: string
  ): void {
    this.logViolation(
      'UI_MUTATION',
      component,
      `UI mutation attempt: ${mutationType} - ${details}`,
      {
        severity: 'HIGH',
        suggestedCorrection: `Ensure ${component} remains static and does not modify props or state after mount`
      }
    );
  }

  // LOG LOGIC INJECTION ATTEMPT
  logLogicInjection(
    component: string,
    injectionType: string,
    details: string
  ): void {
    this.logViolation(
      'LOGIC_INJECTION',
      component,
      `Logic injection detected: ${injectionType} - ${details}`,
      {
        severity: 'CRITICAL',
        suggestedCorrection: `Remove dynamic logic from ${component}. Use only static rendering patterns.`
      }
    );
  }

  // GET VIOLATION METRICS
  getMetrics(): AnomalyMetrics {
    const now = Date.now();
    const oneHourAgo = now - (60 * 60 * 1000);
    const recentViolations = this.violations.filter(v => v.timestamp > oneHourAgo);

    const violationsByType: Record<string, number> = {};
    const violationsByComponent: Record<string, number> = {};
    let criticalViolations = 0;

    this.violations.forEach(violation => {
      violationsByType[violation.type] = (violationsByType[violation.type] || 0) + 1;
      violationsByComponent[violation.component] = (violationsByComponent[violation.component] || 0) + 1;
      
      if (violation.severity === 'CRITICAL') {
        criticalViolations++;
      }
    });

    return {
      totalViolations: this.violations.length,
      violationsByType,
      violationsByComponent,
      lastViolationTime: this.violations.length > 0 ? this.violations[this.violations.length - 1].timestamp : 0,
      averageViolationsPerHour: recentViolations.length,
      criticalViolations
    };
  }

  // GET RECENT VIOLATIONS
  getRecentViolations(limit: number = 50): ViolationLogEntry[] {
    return this.violations.slice(-limit);
  }

  // CLEAR ALL VIOLATIONS
  clearViolations(): void {
    this.violations = [];
    this.saveViolationsToStorage();
    console.log('🧹 ANOMALY WATCHDOG: All violations cleared');
  }

  // EXPORT VIOLATIONS FOR ANALYSIS
  exportViolations(): string {
    return JSON.stringify({
      exportTimestamp: new Date().toISOString(),
      lockdownVersion: '1.9X++',
      totalViolations: this.violations.length,
      metrics: this.getMetrics(),
      violations: this.violations
    }, null, 2);
  }

  // PRIVATE METHODS

  private generateViolationId(): string {
    return `anomaly_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private determineSeverity(type: ViolationLogEntry['type']): ViolationLogEntry['severity'] {
    switch (type) {
      case 'LOGIC_INJECTION':
      case 'ROGUE_RENDER':
        return 'CRITICAL';
      case 'UNAUTHORIZED_PROP':
      case 'UI_MUTATION':
        return 'HIGH';
      case 'SCHEMA_VIOLATION':
        return 'MEDIUM';
      default:
        return 'LOW';
    }
  }

  private getCurrentRoute(): string {
    if (typeof window !== 'undefined') {
      return window.location.pathname;
    }
    return 'Unknown';
  }

  private sanitizeValue(value: any): any {
    if (value === undefined || value === null) return value;
    if (typeof value === 'function') return '[Function]';
    if (typeof value === 'object') {
      try {
        return JSON.parse(JSON.stringify(value));
      } catch {
        return '[Complex Object]';
      }
    }
    return value;
  }

  private generateSuggestion(type: ViolationLogEntry['type'], component: string): string {
    switch (type) {
      case 'UNAUTHORIZED_PROP':
        return `Review the prop schema for ${component} and ensure only approved props are used.`;
      case 'ROGUE_RENDER':
        return `Add ${component} to the approved component registry or remove from render tree.`;
      case 'UI_MUTATION':
        return `Ensure ${component} remains static and immutable after initial render.`;
      case 'LOGIC_INJECTION':
        return `Remove all dynamic logic from ${component}. Use only static rendering patterns.`;
      case 'SCHEMA_VIOLATION':
        return `Validate the data structure against the approved schema for ${component}.`;
      default:
        return `Review the implementation of ${component} for compliance with lockdown rules.`;
    }
  }

  private logToConsole(violation: ViolationLogEntry): void {
    const severityColors = {
      LOW: '#6B7280',      // Gray
      MEDIUM: '#F59E0B',   // Yellow
      HIGH: '#EF4444',     // Red
      CRITICAL: '#DC2626'  // Dark Red
    };

    const color = severityColors[violation.severity];
    
    console.group(`%c🚨 ANOMALY DETECTED [${violation.severity}]`, `color: ${color}; font-weight: bold;`);
    console.log(`%cType: ${violation.type}`, `color: ${color};`);
    console.log(`%cComponent: ${violation.component}`, `color: ${color};`);
    console.log(`%cDetails: ${violation.details}`, `color: ${color};`);
    console.log(`%cTime: ${violation.timestampISO}`, `color: ${color};`);
    console.log(`%cRoute: ${violation.metadata.routeContext}`, `color: ${color};`);
    
    if (violation.suggestedCorrection) {
      console.log(`%c💡 Suggestion: ${violation.suggestedCorrection}`, `color: #10B981;`);
    }
    
    if (violation.stackTrace && process.env.NODE_ENV === 'development') {
      console.log(`%cStack Trace:`, `color: #6B7280;`);
      console.log(violation.stackTrace);
    }
    
    console.groupEnd();
  }

  private triggerCriticalAlert(violation: ViolationLogEntry): void {
    // In development, show browser notification if available
    if (process.env.NODE_ENV === 'development' && typeof window !== 'undefined' && 'Notification' in window) {
      if (Notification.permission === 'granted') {
        new Notification('🚨 CRITICAL LOCKDOWN VIOLATION', {
          body: `${violation.component}: ${violation.details}`,
          icon: '/favicon.ico'
        });
      }
    }

    // Log critical alert
    console.error('🚨🚨🚨 CRITICAL ANOMALY DETECTED 🚨🚨🚨', violation);
  }

  private loadViolationsFromStorage(): void {
    if (typeof window !== 'undefined') {
      try {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
          this.violations = JSON.parse(stored);
        }
      } catch (error) {
        console.warn('Failed to load violations from storage:', error);
      }
    }
  }

  private saveViolationsToStorage(): void {
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(this.storageKey, JSON.stringify(this.violations));
      } catch (error) {
        console.warn('Failed to save violations to storage:', error);
      }
    }
  }

  private setupGlobalErrorHandlers(): void {
    if (typeof window !== 'undefined') {
      // Catch unhandled errors that might indicate logic injection
      window.addEventListener('error', (event) => {
        if (event.error && event.error.message.includes('SENTIENCE') || 
            event.error.message.includes('LOCKDOWN')) {
          this.logViolation(
            'LOGIC_INJECTION',
            'GlobalErrorHandler',
            `Unhandled error: ${event.error.message}`,
            {
              severity: 'CRITICAL',
              stackTrace: event.error.stack
            }
          );
        }
      });

      // Catch unhandled promise rejections
      window.addEventListener('unhandledrejection', (event) => {
        if (event.reason && typeof event.reason === 'object' && 
            event.reason.message && 
            (event.reason.message.includes('SENTIENCE') || event.reason.message.includes('LOCKDOWN'))) {
          this.logViolation(
            'LOGIC_INJECTION',
            'GlobalPromiseHandler',
            `Unhandled promise rejection: ${event.reason.message}`,
            {
              severity: 'CRITICAL'
            }
          );
        }
      });
    }
  }

  private startPeriodicCleanup(): void {
    // Clean up old violations every hour
    setInterval(() => {
      const oneWeekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
      const beforeCount = this.violations.length;
      
      this.violations = this.violations.filter(v => v.timestamp > oneWeekAgo);
      
      if (this.violations.length < beforeCount) {
        this.saveViolationsToStorage();
        console.log(`🧹 ANOMALY WATCHDOG: Cleaned up ${beforeCount - this.violations.length} old violations`);
      }
    }, 60 * 60 * 1000); // Every hour
  }
}

// GLOBAL WATCHDOG INSTANCE
export const anomalyWatchdog = AnomalyWatchdog.getInstance();

// GLOBAL VIOLATION REPORTERS - Available to all components
if (typeof window !== 'undefined') {
  // @ts-ignore - Global anomaly reporter
  window.__AIFOLIO_ANOMALY_WATCHDOG__ = anomalyWatchdog;
  
  // @ts-ignore - Quick violation reporters
  window.__AIFOLIO_LOG_UNAUTHORIZED_PROP__ = (component: string, propKey: string, expectedProps: string[]) => {
    anomalyWatchdog.logUnauthorizedProp(component, propKey, expectedProps);
  };
  
  // @ts-ignore - Rogue render reporter
  window.__AIFOLIO_LOG_ROGUE_RENDER__ = (component: string, details: string) => {
    anomalyWatchdog.logRogueRender(component, window.location.pathname, details);
  };
  
  // @ts-ignore - UI mutation reporter
  window.__AIFOLIO_LOG_UI_MUTATION__ = (component: string, mutationType: string, details: string) => {
    anomalyWatchdog.logUIMutation(component, mutationType, details);
  };
}
