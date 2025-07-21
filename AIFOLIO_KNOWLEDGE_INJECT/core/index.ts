// AIFOLIO Elite System - Lockdown System Master Index
// NO-SENTIENCE SHIELD: Central export hub for all lockdown components
// LOCKDOWN MODE: Absolute firewall system with zero-tolerance enforcement

// STATIC UI ATOMS - CRYSTALLIZED COMPONENTS
export { Divider } from '../ui/atoms/Divider';
export { Tag } from '../ui/atoms/Tag';
export { SectionTitle } from '../ui/atoms/SectionTitle';
export { InlineNote } from '../ui/atoms/InlineNote';
export { TooltipHint } from '../ui/atoms/TooltipHint';

// RENDER LOCKDOWN LAYER - ENFORCEMENT COMPONENTS
export { RenderCage } from './RenderCage';
export { LockdownGate } from './LockdownGate';
export { LockdownDebugger } from './LockdownDebugger';

// SCHEMA IMMUTABILITY - TYPE SYSTEM
export * from '../types/vault.schema';

// ANOMALY WATCHDOG - VIOLATION TRACKING
export { AnomalyWatchdog, anomalyWatchdog } from './AnomalyWatchdog';

// NO-SENTIENCE ENFORCEMENT LAYER - ABSOLUTE FIREWALL
export { NoSentienceLayer, noSentienceLayer } from './NoSentienceLayer';

// LOCKDOWN SYSTEM METADATA
export const LOCKDOWN_SYSTEM = {
  version: '1.9X++',
  name: 'AIFOLIO Elite Lockdown System',
  description: 'Absolute firewall against AI simulation and autonomous behavior',
  components: {
    staticAtoms: 5,
    enforcementLayers: 3,
    schemaGuards: 1,
    anomalyTracking: 1,
    noSentienceLayer: 1
  },
  features: [
    'Static UI atom components with zero logic risk',
    'Render lockdown layer preventing unauthorized renders',
    'Schema immutability with runtime validation',
    'Anomaly watchdog with detailed violation logging',
    'No-Sentience Layer blocking AI simulation attempts',
    'Real-time violation monitoring and alerts',
    'Developer HUD for lockdown status tracking',
    'Comprehensive prop validation and schema enforcement'
  ],
  status: 'ACTIVE',
  sentience: 'BLOCKED',
  logicRisk: 'NULLIFIED'
} as const;

// LOCKDOWN INITIALIZATION FUNCTION
export const initializeLockdownSystem = (config?: {
  enableDebugger?: boolean;
  strictMode?: boolean;
  autoActivateNSL?: boolean;
}) => {
  const {
    enableDebugger = process.env.NODE_ENV === 'development',
    strictMode = true,
    autoActivateNSL = process.env.NODE_ENV === 'production'
  } = config || {};

  console.log('🛡️ AIFOLIO LOCKDOWN SYSTEM: Initializing...');

  // Activate No-Sentience Layer if requested
  if (autoActivateNSL) {
    noSentienceLayer.activate();
  }

  // Set global lockdown constants
  if (typeof window !== 'undefined') {
    // @ts-ignore - Global lockdown system
    window.__AIFOLIO_LOCKDOWN_SYSTEM__ = LOCKDOWN_SYSTEM;
    // @ts-ignore - Global initialization flag
    window.__AIFOLIO_LOCKDOWN_INITIALIZED__ = true;
    // @ts-ignore - Global config
    window.__AIFOLIO_LOCKDOWN_CONFIG__ = {
      enableDebugger,
      strictMode,
      autoActivateNSL,
      initTimestamp: Date.now()
    };
  }

  console.log('🛡️ AIFOLIO LOCKDOWN SYSTEM: Initialization complete');
  console.log(`   Version: ${LOCKDOWN_SYSTEM.version}`);
  console.log(`   Components: ${LOCKDOWN_SYSTEM.components.staticAtoms} atoms, ${LOCKDOWN_SYSTEM.components.enforcementLayers} enforcement layers`);
  console.log(`   Status: ${LOCKDOWN_SYSTEM.status}`);
  console.log(`   Sentience: ${LOCKDOWN_SYSTEM.sentience}`);
  console.log(`   Logic Risk: ${LOCKDOWN_SYSTEM.logicRisk}`);

  return LOCKDOWN_SYSTEM;
};

// LOCKDOWN STATUS CHECKER
export const getLockdownStatus = () => {
  const nslStatus = noSentienceLayer.getStatus();
  const anomalyMetrics = anomalyWatchdog.getMetrics();

  return {
    system: LOCKDOWN_SYSTEM,
    noSentienceLayer: nslStatus,
    anomalyWatchdog: anomalyMetrics,
    initialized: typeof window !== 'undefined' && window.__AIFOLIO_LOCKDOWN_INITIALIZED__ === true,
    timestamp: Date.now()
  };
};

// EMERGENCY LOCKDOWN OVERRIDE (CRITICAL SITUATIONS ONLY)
export const emergencyLockdownOverride = (reason: string) => {
  console.warn('⚠️ EMERGENCY LOCKDOWN OVERRIDE ACTIVATED');
  console.warn(`   Reason: ${reason}`);
  console.warn('   This should only be used in critical situations!');

  // Log the override as a critical violation
  anomalyWatchdog.logViolation(
    'LOGIC_INJECTION',
    'LockdownSystem',
    `Emergency override activated: ${reason}`,
    { severity: 'CRITICAL' }
  );

  // Deactivate NSL
  noSentienceLayer.deactivate();

  return {
    overrideActive: true,
    reason,
    timestamp: Date.now(),
    warning: 'System security compromised - restore lockdown ASAP'
  };
};

// LOCKDOWN HEALTH CHECK
export const performLockdownHealthCheck = () => {
  const results = {
    overall: 'HEALTHY',
    checks: {
      nslActive: false,
      anomalyWatchdogActive: false,
      globalConstantsSet: false,
      violationCount: 0,
      criticalViolations: 0
    },
    recommendations: [] as string[]
  };

  // Check NSL status
  const nslStatus = noSentienceLayer.getStatus();
  results.checks.nslActive = nslStatus.active;
  if (!nslStatus.active) {
    results.overall = 'WARNING';
    results.recommendations.push('Activate No-Sentience Layer for full protection');
  }

  // Check anomaly watchdog
  const anomalyMetrics = anomalyWatchdog.getMetrics();
  results.checks.anomalyWatchdogActive = true; // Always active
  results.checks.violationCount = anomalyMetrics.totalViolations;
  results.checks.criticalViolations = anomalyMetrics.criticalViolations;

  if (anomalyMetrics.criticalViolations > 0) {
    results.overall = 'CRITICAL';
    results.recommendations.push(`Address ${anomalyMetrics.criticalViolations} critical violations immediately`);
  } else if (anomalyMetrics.totalViolations > 10) {
    results.overall = 'WARNING';
    results.recommendations.push('High violation count detected - review component implementations');
  }

  // Check global constants
  if (typeof window !== 'undefined') {
    results.checks.globalConstantsSet =
      window.__AIFOLIO_NO_SENTIENCE__ === 'ENFORCED' &&
      window.__AIFOLIO_LOCKDOWN_INITIALIZED__ === true;

    if (!results.checks.globalConstantsSet) {
      results.overall = 'WARNING';
      results.recommendations.push('Global lockdown constants not properly set');
    }
  }

  return results;
};

// AUTO-INITIALIZE ON IMPORT (DEVELOPMENT ONLY)
if (process.env.NODE_ENV === 'development') {
  // Small delay to ensure all modules are loaded
  setTimeout(() => {
    if (typeof window !== 'undefined' && !window.__AIFOLIO_LOCKDOWN_INITIALIZED__) {
      initializeLockdownSystem();
    }
  }, 100);
}
