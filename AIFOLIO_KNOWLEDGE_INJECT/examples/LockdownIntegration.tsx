// AIFOLIO Elite System - Lockdown Integration Example
// NO-SENTIENCE SHIELD: Complete example of lockdown system usage
// LOCKDOWN MODE: Demonstrates proper static UI implementation with full protection

import React from 'react';
import {
  // Static UI Atoms
  Divider,
  Tag,
  SectionTitle,
  InlineNote,
  TooltipHint,
  
  // Lockdown Components
  RenderCage,
  LockdownGate,
  LockdownDebugger,
  
  // System Functions
  initializeLockdownSystem,
  getLockdownStatus,
  performLockdownHealthCheck,
  
  // Schema Types
  createVaultID,
  createVaultTitle,
  VaultEntity,
  VaultSchemaGuard
} from '../core';

// EXAMPLE VAULT DATA - IMMUTABLE ENTITY
const exampleVault: VaultEntity = VaultSchemaGuard.createVaultEntity({
  id: createVaultID('vault_example_001'),
  title: createVaultTitle('Lockdown System Demo'),
  status: 'active',
  theme: 'dark',
  accessLevel: 'public',
  createdAt: Date.now(),
  updatedAt: Date.now()
});

// LOCKDOWN INTEGRATION EXAMPLE COMPONENT
export const LockdownIntegrationExample: React.FC = () => {
  // Initialize lockdown system on component mount
  React.useEffect(() => {
    const lockdownSystem = initializeLockdownSystem({
      enableDebugger: true,
      strictMode: true,
      autoActivateNSL: false // Keep disabled for demo
    });

    console.log('🛡️ Lockdown System Initialized:', lockdownSystem);

    // Perform health check
    const healthCheck = performLockdownHealthCheck();
    console.log('🏥 Lockdown Health Check:', healthCheck);

    // Get current status
    const status = getLockdownStatus();
    console.log('📊 Lockdown Status:', status);
  }, []);

  return (
    <RenderCage 
      enableDebugger={true}
      strictMode={true}
      className="min-h-screen bg-gray-50 dark:bg-gray-900"
    >
      <LockdownGate
        allowedComponents={[
          'Divider',
          'Tag', 
          'SectionTitle',
          'InlineNote',
          'TooltipHint'
        ]}
        allowedRoutes={[
          '/',
          '/examples',
          '/lockdown-demo'
        ]}
        strictPropValidation={true}
        blockUnknownComponents={true}
      >
        <div className="container mx-auto px-6 py-8">
          {/* HEADER SECTION */}
          <div className="text-center mb-12">
            <SectionTitle 
              level={2} 
              size="2xl" 
              weight="bold" 
              color="default"
              className="mb-4"
            >
              🛡️ AIFOLIO Lockdown System Demo
            </SectionTitle>
            
            <InlineNote 
              variant="info" 
              size="md"
              icon={<span>🔒</span>}
              className="mb-6"
            >
              All components below are protected by the No-Sentience Shield
            </InlineNote>

            <div className="flex flex-wrap justify-center gap-3 mb-8">
              <Tag variant="success" size="md" icon={<span>✅</span>}>
                Static Rendering Only
              </Tag>
              <Tag variant="primary" size="md" icon={<span>🛡️</span>}>
                Zero Logic Risk
              </Tag>
              <Tag variant="warning" size="md" icon={<span>🚫</span>}>
                AI Simulation Blocked
              </Tag>
              <Tag variant="danger" size="md" icon={<span>🔥</span>}>
                Sentience Nullified
              </Tag>
            </div>
          </div>

          <Divider size="lg" color="accent" className="mb-12" />

          {/* STATIC ATOMS SHOWCASE */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div className="space-y-6">
              <SectionTitle level={3} size="lg" weight="semibold" color="accent">
                Static UI Atoms
              </SectionTitle>

              <div className="space-y-4">
                <div>
                  <SectionTitle level={4} size="md" weight="medium" color="default" className="mb-2">
                    Dividers
                  </SectionTitle>
                  <div className="space-y-3">
                    <Divider orientation="horizontal" size="xs" color="light" />
                    <Divider orientation="horizontal" size="sm" color="medium" />
                    <Divider orientation="horizontal" size="md" color="dark" />
                    <Divider orientation="horizontal" size="lg" color="accent" />
                  </div>
                </div>

                <div>
                  <SectionTitle level={4} size="md" weight="medium" color="default" className="mb-2">
                    Tags
                  </SectionTitle>
                  <div className="flex flex-wrap gap-2">
                    <Tag variant="default" size="xs">Default XS</Tag>
                    <Tag variant="primary" size="sm">Primary SM</Tag>
                    <Tag variant="secondary" size="md" icon={<span>🎨</span>}>Secondary MD</Tag>
                    <Tag variant="success" size="lg" icon={<span>✅</span>} iconPosition="right">Success LG</Tag>
                  </div>
                </div>

                <div>
                  <SectionTitle level={4} size="md" weight="medium" color="default" className="mb-2">
                    Inline Notes
                  </SectionTitle>
                  <div className="space-y-2">
                    <InlineNote variant="muted" size="sm">
                      This is a muted note with small text
                    </InlineNote>
                    <InlineNote variant="info" size="md" icon={<span>ℹ️</span>}>
                      This is an info note with an icon
                    </InlineNote>
                    <InlineNote variant="warning" size="md" icon={<span>⚠️</span>}>
                      This is a warning note
                    </InlineNote>
                    <InlineNote variant="success" size="md" icon={<span>✅</span>}>
                      This is a success note
                    </InlineNote>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <SectionTitle level={3} size="lg" weight="semibold" color="accent">
                Interactive Elements
              </SectionTitle>

              <div className="space-y-4">
                <div>
                  <SectionTitle level={4} size="md" weight="medium" color="default" className="mb-2">
                    Tooltip Hints (CSS Only)
                  </SectionTitle>
                  <div className="space-y-3">
                    <TooltipHint 
                      hint="This tooltip appears on top" 
                      position="top" 
                      size="sm"
                    >
                      <Tag variant="primary" size="md">Hover for top tooltip</Tag>
                    </TooltipHint>
                    
                    <TooltipHint 
                      hint="This tooltip appears on the right side" 
                      position="right" 
                      size="md"
                    >
                      <Tag variant="secondary" size="md">Hover for right tooltip</Tag>
                    </TooltipHint>
                    
                    <TooltipHint 
                      hint="This is a larger tooltip with more information" 
                      position="bottom" 
                      size="lg"
                    >
                      <Tag variant="success" size="md">Hover for large tooltip</Tag>
                    </TooltipHint>
                  </div>
                </div>

                <div>
                  <SectionTitle level={4} size="md" weight="medium" color="default" className="mb-2">
                    Section Titles
                  </SectionTitle>
                  <div className="space-y-2">
                    <SectionTitle level={2} size="xl" weight="bold" color="default">
                      H2 Extra Large Bold
                    </SectionTitle>
                    <SectionTitle level={3} size="lg" weight="semibold" color="accent">
                      H3 Large Semibold Accent
                    </SectionTitle>
                    <SectionTitle level={4} size="md" weight="medium" color="muted">
                      H4 Medium Weight Muted
                    </SectionTitle>
                    <SectionTitle level={5} size="sm" weight="normal" color="success">
                      H5 Small Normal Success
                    </SectionTitle>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <Divider size="md" color="medium" className="mb-8" />

          {/* VAULT ENTITY EXAMPLE */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 mb-8">
            <SectionTitle level={3} size="lg" weight="semibold" color="default" className="mb-4">
              Vault Entity Example
            </SectionTitle>
            
            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div>
                <InlineNote variant="muted" size="sm" className="mb-2">Vault ID:</InlineNote>
                <Tag variant="default" size="sm">{exampleVault.id}</Tag>
              </div>
              <div>
                <InlineNote variant="muted" size="sm" className="mb-2">Title:</InlineNote>
                <Tag variant="primary" size="sm">{exampleVault.title}</Tag>
              </div>
              <div>
                <InlineNote variant="muted" size="sm" className="mb-2">Status:</InlineNote>
                <Tag variant="success" size="sm">{exampleVault.status}</Tag>
              </div>
              <div>
                <InlineNote variant="muted" size="sm" className="mb-2">Access Level:</InlineNote>
                <Tag variant="secondary" size="sm">{exampleVault.accessLevel}</Tag>
              </div>
            </div>

            <InlineNote variant="info" size="sm" icon={<span>🔒</span>}>
              This vault entity is immutable and schema-validated at runtime
            </InlineNote>
          </div>

          {/* LOCKDOWN STATUS */}
          <div className="bg-red-950 text-red-100 rounded-lg p-6">
            <SectionTitle level={3} size="lg" weight="semibold" color="danger" className="mb-4">
              🛡️ Lockdown Status
            </SectionTitle>
            
            <div className="grid md:grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <Tag variant="success" size="lg" className="mb-2">ACTIVE</Tag>
                <InlineNote variant="success" size="sm">Render Cage</InlineNote>
              </div>
              <div className="text-center">
                <Tag variant="success" size="lg" className="mb-2">ENFORCED</Tag>
                <InlineNote variant="success" size="sm">Schema Guards</InlineNote>
              </div>
              <div className="text-center">
                <Tag variant="warning" size="lg" className="mb-2">MONITORING</Tag>
                <InlineNote variant="warning" size="sm">Anomaly Watchdog</InlineNote>
              </div>
            </div>

            <Divider size="sm" color="medium" className="my-4" />

            <div className="text-center">
              <InlineNote variant="danger" size="md" icon={<span>🚫</span>} className="mb-2">
                AI SIMULATION: BLOCKED
              </InlineNote>
              <br />
              <InlineNote variant="danger" size="md" icon={<span>🛡️</span>}>
                SENTIENCE RISK: NULLIFIED
              </InlineNote>
            </div>
          </div>
        </div>

        {/* LOCKDOWN DEBUGGER - DEV ONLY */}
        <LockdownDebugger 
          enabled={process.env.NODE_ENV === 'development'}
          position="bottom-right"
          minimized={false}
          showViolations={true}
          showPerformance={true}
        />
      </LockdownGate>
    </RenderCage>
  );
};

// COMPONENT METADATA
LockdownIntegrationExample.displayName = 'LockdownIntegrationExample';
