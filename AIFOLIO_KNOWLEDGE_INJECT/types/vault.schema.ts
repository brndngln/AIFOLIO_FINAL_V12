// AIFOLIO Elite System - Vault Schema Immutability
// NO-SENTIENCE SHIELD: Lock allowed props and enforce runtime schema guards
// LOCKDOWN MODE: TypeScript + Runtime validation for absolute prop control

// IMMUTABLE VAULT CORE TYPES - NO MUTATIONS ALLOWED
export type VaultID = string & { readonly __brand: 'VaultID' };
export type VaultStatus = 'active' | 'archived' | 'locked' | 'pending' | 'error';
export type VaultTheme = 'light' | 'dark' | 'auto' | 'system';
export type VaultTitle = string & { readonly __brand: 'VaultTitle' };
export type AccessLevel = 'public' | 'private' | 'restricted' | 'admin';

// VAULT COMPONENT PROP SCHEMAS - CRYSTALLIZED INTERFACES
export interface VaultDividerProps {
  readonly orientation?: 'horizontal' | 'vertical';
  readonly size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  readonly color?: 'light' | 'medium' | 'dark' | 'accent';
  readonly className?: string;
}

export interface VaultTagProps {
  readonly children: React.ReactNode;
  readonly variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
  readonly size?: 'xs' | 'sm' | 'md' | 'lg';
  readonly icon?: React.ReactNode;
  readonly iconPosition?: 'left' | 'right';
  readonly className?: string;
}

export interface VaultSectionTitleProps {
  readonly children: React.ReactNode;
  readonly level?: 2 | 3 | 4 | 5 | 6;
  readonly size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  readonly weight?: 'normal' | 'medium' | 'semibold' | 'bold';
  readonly color?: 'default' | 'muted' | 'accent' | 'success' | 'warning' | 'danger';
  readonly className?: string;
}

export interface VaultInlineNoteProps {
  readonly children: React.ReactNode;
  readonly variant?: 'muted' | 'info' | 'success' | 'warning' | 'danger';
  readonly size?: 'xs' | 'sm' | 'md';
  readonly icon?: React.ReactNode;
  readonly className?: string;
}

export interface VaultTooltipHintProps {
  readonly children: React.ReactNode;
  readonly hint: string;
  readonly position?: 'top' | 'bottom' | 'left' | 'right';
  readonly size?: 'sm' | 'md' | 'lg';
  readonly className?: string;
}

// VAULT CORE ENTITY SCHEMA - IMMUTABLE DATA STRUCTURE
export interface VaultEntity {
  readonly id: VaultID;
  readonly title: VaultTitle;
  readonly status: VaultStatus;
  readonly theme: VaultTheme;
  readonly accessLevel: AccessLevel;
  readonly createdAt: number;
  readonly updatedAt: number;
  readonly metadata: {
    readonly version: string;
    readonly checksum: string;
    readonly lockdownVersion: string;
  };
}

// VAULT COMPONENT REGISTRY - APPROVED COMPONENTS ONLY
export const VAULT_COMPONENT_REGISTRY = {
  Divider: 'VaultDividerProps',
  Tag: 'VaultTagProps',
  SectionTitle: 'VaultSectionTitleProps',
  InlineNote: 'VaultInlineNoteProps',
  TooltipHint: 'VaultTooltipHintProps'
} as const;

// PROP VALIDATION SCHEMAS - RUNTIME GUARDS
export const VAULT_PROP_SCHEMAS = {
  VaultDividerProps: ['orientation', 'size', 'color', 'className'],
  VaultTagProps: ['children', 'variant', 'size', 'icon', 'iconPosition', 'className'],
  VaultSectionTitleProps: ['children', 'level', 'size', 'weight', 'color', 'className'],
  VaultInlineNoteProps: ['children', 'variant', 'size', 'icon', 'className'],
  VaultTooltipHintProps: ['children', 'hint', 'position', 'size', 'className']
} as const;

// SCHEMA VALIDATION UTILITIES - RUNTIME ENFORCEMENT
export class VaultSchemaGuard {
  private static readonly VIOLATION_LOG_KEY = 'aifolio_schema_violations';

  // VALIDATE COMPONENT PROPS AT RUNTIME
  static validateProps<T extends keyof typeof VAULT_PROP_SCHEMAS>(
    componentName: T,
    props: Record<string, any>
  ): boolean {
    const allowedProps = VAULT_PROP_SCHEMAS[componentName];
    const propKeys = Object.keys(props);

    for (const key of propKeys) {
      if (!allowedProps.includes(key as any)) {
        this.logViolation('UNAUTHORIZED_PROP', componentName, `Prop "${key}" not allowed`);
        
        if (process.env.NODE_ENV === 'development') {
          throw new Error(`🚨 SCHEMA VIOLATION: Prop "${key}" not allowed in ${componentName}`);
        }
        
        return false;
      }
    }

    return true;
  }

  // VALIDATE VAULT ENTITY STRUCTURE
  static validateVaultEntity(entity: any): entity is VaultEntity {
    const requiredFields = ['id', 'title', 'status', 'theme', 'accessLevel', 'createdAt', 'updatedAt', 'metadata'];
    
    for (const field of requiredFields) {
      if (!(field in entity)) {
        this.logViolation('INVALID_ENTITY', 'VaultEntity', `Missing required field: ${field}`);
        return false;
      }
    }

    // Validate enum values
    const validStatuses: VaultStatus[] = ['active', 'archived', 'locked', 'pending', 'error'];
    const validThemes: VaultTheme[] = ['light', 'dark', 'auto', 'system'];
    const validAccessLevels: AccessLevel[] = ['public', 'private', 'restricted', 'admin'];

    if (!validStatuses.includes(entity.status)) {
      this.logViolation('INVALID_ENTITY', 'VaultEntity', `Invalid status: ${entity.status}`);
      return false;
    }

    if (!validThemes.includes(entity.theme)) {
      this.logViolation('INVALID_ENTITY', 'VaultEntity', `Invalid theme: ${entity.theme}`);
      return false;
    }

    if (!validAccessLevels.includes(entity.accessLevel)) {
      this.logViolation('INVALID_ENTITY', 'VaultEntity', `Invalid accessLevel: ${entity.accessLevel}`);
      return false;
    }

    return true;
  }

  // CREATE IMMUTABLE VAULT ENTITY
  static createVaultEntity(data: Omit<VaultEntity, 'metadata'>): VaultEntity {
    const entity: VaultEntity = {
      ...data,
      metadata: {
        version: '1.9X++',
        checksum: this.generateChecksum(data),
        lockdownVersion: process.env.AIFOLIO_LOCKDOWN_VERSION || '1.9X++'
      }
    };

    if (!this.validateVaultEntity(entity)) {
      throw new Error('🚨 SCHEMA VIOLATION: Invalid vault entity structure');
    }

    return Object.freeze(entity); // Make immutable
  }

  // GENERATE ENTITY CHECKSUM
  private static generateChecksum(data: any): string {
    const str = JSON.stringify(data, Object.keys(data).sort());
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(36);
  }

  // LOG SCHEMA VIOLATIONS
  private static logViolation(type: string, component: string, details: string): void {
    const violation = {
      id: `schema_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      type,
      component,
      details,
      stackTrace: new Error().stack
    };

    console.error(`🚨 SCHEMA VIOLATION [${type}]:`, violation);

    // Store in localStorage for debugging
    if (typeof window !== 'undefined') {
      try {
        const existing = JSON.parse(localStorage.getItem(this.VIOLATION_LOG_KEY) || '[]');
        existing.push(violation);
        localStorage.setItem(this.VIOLATION_LOG_KEY, JSON.stringify(existing.slice(-50)));
      } catch (error) {
        console.warn('Failed to log schema violation:', error);
      }
    }
  }
}

// VAULT BRAND CREATORS - TYPE-SAFE CONSTRUCTORS
export const createVaultID = (id: string): VaultID => {
  if (!id || typeof id !== 'string' || id.length < 1) {
    throw new Error('🚨 SCHEMA VIOLATION: VaultID must be a non-empty string');
  }
  return id as VaultID;
};

export const createVaultTitle = (title: string): VaultTitle => {
  if (!title || typeof title !== 'string' || title.length < 1 || title.length > 200) {
    throw new Error('🚨 SCHEMA VIOLATION: VaultTitle must be 1-200 characters');
  }
  return title as VaultTitle;
};

// IMMUTABLE CONSTANTS - NO-SENTIENCE ENFORCEMENT
export const VAULT_CONSTANTS = Object.freeze({
  MAX_TITLE_LENGTH: 200,
  MAX_COMPONENTS_PER_VAULT: 100,
  LOCKDOWN_VERSION: '1.9X++',
  NO_SENTIENCE_ENFORCED: true,
  SCHEMA_VERSION: '1.0.0'
} as const);

// RUNTIME SCHEMA ENFORCEMENT - GLOBAL GUARD
if (typeof window !== 'undefined') {
  // @ts-ignore - Global schema guard
  window.__AIFOLIO_SCHEMA_GUARD__ = VaultSchemaGuard;
  
  // Inject schema validation into global scope
  // @ts-ignore - Global prop validator
  window.__AIFOLIO_VALIDATE_PROPS__ = (componentName: string, props: any) => {
    if (componentName in VAULT_PROP_SCHEMAS) {
      return VaultSchemaGuard.validateProps(componentName as any, props);
    }
    return true;
  };
}
