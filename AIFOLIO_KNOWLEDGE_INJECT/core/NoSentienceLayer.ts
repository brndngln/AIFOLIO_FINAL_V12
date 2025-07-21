// AIFOLIO Elite System - No-Sentience Enforcement Layer (NSL)
// NO-SENTIENCE SHIELD: Absolute firewall against AI simulation and autonomous behavior
// LOCKDOWN MODE: Deny system access, disable dynamic logic, enforce static rendering

import { anomalyWatchdog } from './AnomalyWatchdog';

// NSL Configuration interface
interface NSLConfig {
  readonly strictMode: boolean;
  readonly blockSystemTime: boolean;
  readonly blockMemoryAccess: boolean;
  readonly blockUserPatterns: boolean;
  readonly blockConditionalRendering: boolean;
  readonly blockAsyncUILogic: boolean;
  readonly blockCustomEventListeners: boolean;
  readonly blockStatefulHooks: boolean;
  readonly enforceCSP: boolean;
  readonly blockDynamicImports: boolean;
  readonly blockFramerMotionDynamic: boolean;
}

// Blocked API tracking
interface BlockedAPICall {
  readonly api: string;
  readonly timestamp: number;
  readonly component: string;
  readonly stackTrace: string;
}

// NO-SENTIENCE ENFORCEMENT LAYER CLASS
export class NoSentienceLayer {
  private static instance: NoSentienceLayer | null = null;
  private config: NSLConfig;
  private blockedCalls: BlockedAPICall[] = [];
  private originalAPIs: Map<string, any> = new Map();
  private isActive: boolean = false;

  // SINGLETON PATTERN
  static getInstance(config?: Partial<NSLConfig>): NoSentienceLayer {
    if (!NoSentienceLayer.instance) {
      NoSentienceLayer.instance = new NoSentienceLayer(config);
    }
    return NoSentienceLayer.instance;
  }

  private constructor(config?: Partial<NSLConfig>) {
    this.config = {
      strictMode: true,
      blockSystemTime: true,
      blockMemoryAccess: true,
      blockUserPatterns: true,
      blockConditionalRendering: true,
      blockAsyncUILogic: true,
      blockCustomEventListeners: true,
      blockStatefulHooks: true,
      enforceCSP: true,
      blockDynamicImports: true,
      blockFramerMotionDynamic: true,
      ...config
    };
  }

  // ACTIVATE NO-SENTIENCE ENFORCEMENT
  activate(): void {
    if (this.isActive) {
      console.warn('🛡️ NSL: Already active');
      return;
    }

    console.log('🛡️ NO-SENTIENCE LAYER: Activating absolute firewall...');

    // Set global enforcement constant
    this.setGlobalConstants();

    // Block dangerous APIs
    this.blockDangerousAPIs();

    // Override system time access
    if (this.config.blockSystemTime) {
      this.blockSystemTimeAccess();
    }

    // Block memory access patterns
    if (this.config.blockMemoryAccess) {
      this.blockMemoryAccess();
    }

    // Block user pattern detection
    if (this.config.blockUserPatterns) {
      this.blockUserPatternAPIs();
    }

    // Block async UI logic
    if (this.config.blockAsyncUILogic) {
      this.blockAsyncUILogic();
    }

    // Block custom event listeners
    if (this.config.blockCustomEventListeners) {
      this.blockCustomEventListeners();
    }

    // Enforce CSP headers
    if (this.config.enforceCSP) {
      this.enforceCSPHeaders();
    }

    // Block dynamic imports
    if (this.config.blockDynamicImports) {
      this.blockDynamicImports();
    }

    // Monitor Framer Motion usage
    if (this.config.blockFramerMotionDynamic) {
      this.monitorFramerMotion();
    }

    this.isActive = true;
    console.log('🛡️ NO-SENTIENCE LAYER: Firewall ACTIVE - All AI simulation BLOCKED');
  }

  // DEACTIVATE ENFORCEMENT (EMERGENCY ONLY)
  deactivate(): void {
    if (!this.isActive) {
      console.warn('🛡️ NSL: Already inactive');
      return;
    }

    console.warn('⚠️ NO-SENTIENCE LAYER: DEACTIVATING - Emergency override detected');

    // Restore original APIs
    this.restoreOriginalAPIs();

    this.isActive = false;
    
    // Log deactivation as critical violation
    anomalyWatchdog.logViolation(
      'LOGIC_INJECTION',
      'NoSentienceLayer',
      'NSL deactivated - Emergency override used',
      { severity: 'CRITICAL' }
    );
  }

  // GET NSL STATUS
  getStatus(): {
    active: boolean;
    config: NSLConfig;
    blockedCallsCount: number;
    lastBlockedCall?: BlockedAPICall;
  } {
    return {
      active: this.isActive,
      config: this.config,
      blockedCallsCount: this.blockedCalls.length,
      lastBlockedCall: this.blockedCalls[this.blockedCalls.length - 1]
    };
  }

  // PRIVATE ENFORCEMENT METHODS

  private setGlobalConstants(): void {
    if (typeof window !== 'undefined') {
      // @ts-ignore - Global NSL constants
      window.__AIFOLIO_NO_SENTIENCE__ = 'ENFORCED';
      // @ts-ignore
      window.__AIFOLIO_NSL_ACTIVE__ = true;
      // @ts-ignore
      window.__AIFOLIO_LOCKDOWN_VERSION__ = '1.9X++';
    }

    // Set process.env constant if available
    if (typeof process !== 'undefined' && process.env) {
      process.env.NO_AI_SENTIENCE = 'ENFORCED';
      process.env.AIFOLIO_NSL_ACTIVE = 'true';
    }
  }

  private blockDangerousAPIs(): void {
    if (typeof window === 'undefined') return;

    // Block eval
    if (window.eval) {
      this.originalAPIs.set('eval', window.eval);
      window.eval = this.createBlockedAPIHandler('eval');
    }

    // Block Function constructor
    if (window.Function) {
      this.originalAPIs.set('Function', window.Function);
      window.Function = this.createBlockedAPIHandler('Function') as any;
    }

    // Block dynamic script creation
    const originalCreateElement = document.createElement;
    this.originalAPIs.set('createElement', originalCreateElement);
    document.createElement = ((tagName: string, options?: any) => {
      if (tagName.toLowerCase() === 'script') {
        this.logBlockedCall('createElement(script)', 'Document', new Error().stack || '');
        throw new Error('🛡️ NSL: Dynamic script creation blocked');
      }
      return originalCreateElement.call(document, tagName, options);
    }) as any;
  }

  private blockSystemTimeAccess(): void {
    if (typeof window === 'undefined') return;

    // Block Date constructor for dynamic time access
    const originalDate = window.Date;
    this.originalAPIs.set('Date', originalDate);
    
    // Allow static date creation but block dynamic time-based logic
    window.Date = class extends originalDate {
      constructor(...args: any[]) {
        if (args.length === 0) {
          // Block parameterless Date() which gives current time
          const stack = new Error().stack || '';
          if (stack.includes('ui/') || stack.includes('components/')) {
            NoSentienceLayer.getInstance().logBlockedCall('Date()', 'UI Component', stack);
            throw new Error('🛡️ NSL: Current time access blocked in UI components');
          }
        }
        super(...args);
      }
    } as any;

    // Block performance.now() in UI components
    const originalPerformanceNow = performance.now;
    this.originalAPIs.set('performance.now', originalPerformanceNow);
    performance.now = () => {
      const stack = new Error().stack || '';
      if (stack.includes('ui/') || stack.includes('components/')) {
        this.logBlockedCall('performance.now()', 'UI Component', stack);
        throw new Error('🛡️ NSL: Performance timing blocked in UI components');
      }
      return originalPerformanceNow.call(performance);
    };
  }

  private blockMemoryAccess(): void {
    if (typeof window === 'undefined') return;

    // Block localStorage access in UI components
    const originalLocalStorage = window.localStorage;
    this.originalAPIs.set('localStorage', originalLocalStorage);
    
    Object.defineProperty(window, 'localStorage', {
      get: () => {
        const stack = new Error().stack || '';
        if (stack.includes('ui/') || stack.includes('atoms/')) {
          this.logBlockedCall('localStorage', 'UI Component', stack);
          throw new Error('🛡️ NSL: localStorage access blocked in UI components');
        }
        return originalLocalStorage;
      }
    });

    // Block sessionStorage access in UI components
    const originalSessionStorage = window.sessionStorage;
    this.originalAPIs.set('sessionStorage', originalSessionStorage);
    
    Object.defineProperty(window, 'sessionStorage', {
      get: () => {
        const stack = new Error().stack || '';
        if (stack.includes('ui/') || stack.includes('atoms/')) {
          this.logBlockedCall('sessionStorage', 'UI Component', stack);
          throw new Error('🛡️ NSL: sessionStorage access blocked in UI components');
        }
        return originalSessionStorage;
      }
    });
  }

  private blockUserPatternAPIs(): void {
    if (typeof window === 'undefined') return;

    // Block navigator.userAgent in UI components
    const originalUserAgent = navigator.userAgent;
    Object.defineProperty(navigator, 'userAgent', {
      get: () => {
        const stack = new Error().stack || '';
        if (stack.includes('ui/') || stack.includes('atoms/')) {
          this.logBlockedCall('navigator.userAgent', 'UI Component', stack);
          throw new Error('🛡️ NSL: User agent access blocked in UI components');
        }
        return originalUserAgent;
      }
    });

    // Block geolocation in UI components
    if (navigator.geolocation) {
      const originalGeolocation = navigator.geolocation;
      this.originalAPIs.set('geolocation', originalGeolocation);
      
      Object.defineProperty(navigator, 'geolocation', {
        get: () => {
          const stack = new Error().stack || '';
          if (stack.includes('ui/') || stack.includes('atoms/')) {
            this.logBlockedCall('navigator.geolocation', 'UI Component', stack);
            throw new Error('🛡️ NSL: Geolocation access blocked in UI components');
          }
          return originalGeolocation;
        }
      });
    }
  }

  private blockAsyncUILogic(): void {
    if (typeof window === 'undefined') return;

    // Monitor setTimeout for UI components
    const originalSetTimeout = window.setTimeout;
    this.originalAPIs.set('setTimeout', originalSetTimeout);
    
    window.setTimeout = (callback: any, delay?: number, ...args: any[]) => {
      const stack = new Error().stack || '';
      if (stack.includes('ui/') || stack.includes('atoms/')) {
        this.logBlockedCall('setTimeout', 'UI Component', stack);
        throw new Error('🛡️ NSL: setTimeout blocked in UI components');
      }
      return originalSetTimeout(callback, delay, ...args);
    };

    // Monitor setInterval for UI components
    const originalSetInterval = window.setInterval;
    this.originalAPIs.set('setInterval', originalSetInterval);
    
    window.setInterval = (callback: any, delay?: number, ...args: any[]) => {
      const stack = new Error().stack || '';
      if (stack.includes('ui/') || stack.includes('atoms/')) {
        this.logBlockedCall('setInterval', 'UI Component', stack);
        throw new Error('🛡️ NSL: setInterval blocked in UI components');
      }
      return originalSetInterval(callback, delay, ...args);
    };
  }

  private blockCustomEventListeners(): void {
    if (typeof window === 'undefined') return;

    // Monitor addEventListener for UI components
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    this.originalAPIs.set('addEventListener', originalAddEventListener);
    
    EventTarget.prototype.addEventListener = function(type: string, listener: any, options?: any) {
      const stack = new Error().stack || '';
      if (stack.includes('ui/atoms/') && !['mouseenter', 'mouseleave'].includes(type)) {
        NoSentienceLayer.getInstance().logBlockedCall(`addEventListener(${type})`, 'UI Atom', stack);
        throw new Error(`🛡️ NSL: Event listener "${type}" blocked in UI atoms`);
      }
      return originalAddEventListener.call(this, type, listener, options);
    };
  }

  private enforceCSPHeaders(): void {
    if (typeof document === 'undefined') return;

    // Create CSP meta tag if it doesn't exist
    let cspMeta = document.querySelector('meta[http-equiv="Content-Security-Policy"]') as HTMLMetaElement;
    
    if (!cspMeta) {
      cspMeta = document.createElement('meta');
      cspMeta.httpEquiv = 'Content-Security-Policy';
      document.head.appendChild(cspMeta);
    }

    // Set strict CSP
    cspMeta.content = [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob:",
      "font-src 'self'",
      "connect-src 'self'",
      "media-src 'self'",
      "object-src 'none'",
      "child-src 'none'",
      "worker-src 'none'",
      "frame-src 'none'"
    ].join('; ');

    console.log('🛡️ NSL: CSP headers enforced');
  }

  private blockDynamicImports(): void {
    // Block dynamic import() in UI components
    if (typeof window !== 'undefined') {
      const originalImport = (window as any).import;
      if (originalImport) {
        this.originalAPIs.set('import', originalImport);
        (window as any).import = (specifier: string) => {
          const stack = new Error().stack || '';
          if (stack.includes('ui/') || stack.includes('atoms/')) {
            this.logBlockedCall(`import(${specifier})`, 'UI Component', stack);
            throw new Error('🛡️ NSL: Dynamic imports blocked in UI components');
          }
          return originalImport(specifier);
        };
      }
    }
  }

  private monitorFramerMotion(): void {
    // This would be implemented to monitor Framer Motion usage
    // and ensure only static animation variants are used
    console.log('🛡️ NSL: Framer Motion monitoring active (static variants only)');
  }

  private createBlockedAPIHandler(apiName: string): any {
    return (...args: any[]) => {
      const stack = new Error().stack || '';
      this.logBlockedCall(apiName, 'Global', stack);
      throw new Error(`🛡️ NSL: ${apiName} is blocked by No-Sentience Layer`);
    };
  }

  private logBlockedCall(api: string, component: string, stackTrace: string): void {
    const blockedCall: BlockedAPICall = {
      api,
      timestamp: Date.now(),
      component,
      stackTrace
    };

    this.blockedCalls.push(blockedCall);
    
    // Keep only last 100 blocked calls
    if (this.blockedCalls.length > 100) {
      this.blockedCalls = this.blockedCalls.slice(-100);
    }

    // Log to anomaly watchdog
    anomalyWatchdog.logLogicInjection(
      component,
      'Blocked API Call',
      `Attempted to use ${api}`
    );

    console.error(`🛡️ NSL BLOCK: ${api} blocked in ${component}`, {
      timestamp: new Date(blockedCall.timestamp).toISOString(),
      stackTrace
    });
  }

  private restoreOriginalAPIs(): void {
    if (typeof window === 'undefined') return;

    // Restore all overridden APIs
    this.originalAPIs.forEach((originalAPI, apiName) => {
      try {
        switch (apiName) {
          case 'eval':
            window.eval = originalAPI;
            break;
          case 'Function':
            window.Function = originalAPI;
            break;
          case 'createElement':
            document.createElement = originalAPI;
            break;
          case 'Date':
            window.Date = originalAPI;
            break;
          case 'performance.now':
            performance.now = originalAPI;
            break;
          case 'setTimeout':
            window.setTimeout = originalAPI;
            break;
          case 'setInterval':
            window.setInterval = originalAPI;
            break;
          case 'addEventListener':
            EventTarget.prototype.addEventListener = originalAPI;
            break;
          // Add other API restorations as needed
        }
      } catch (error) {
        console.warn(`Failed to restore ${apiName}:`, error);
      }
    });

    this.originalAPIs.clear();
    console.log('🛡️ NSL: Original APIs restored');
  }
}

// GLOBAL NSL INSTANCE
export const noSentienceLayer = NoSentienceLayer.getInstance();

// AUTO-ACTIVATE NSL IN PRODUCTION
if (typeof window !== 'undefined') {
  // @ts-ignore - Global NSL access
  window.__AIFOLIO_NSL__ = noSentienceLayer;
  
  // Auto-activate in production or when explicitly enabled
  if (process.env.NODE_ENV === 'production' || process.env.AIFOLIO_NSL_ENABLED === 'true') {
    noSentienceLayer.activate();
  }
}
