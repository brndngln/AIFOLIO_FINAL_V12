/**
 * AIFOLIO™ System Configuration
 * Elite modular architecture - System-wide configuration management
 */

import { Logger } from '../../lib/utils/logger';

export interface SystemConfiguration {
  api: {
    baseUrl: string;
    timeout: number;
    retries: number;
  };
  features: {
    darkMode: boolean;
    analytics: boolean;
    notifications: boolean;
    autoSave: boolean;
  };
  security: {
    sessionTimeout: number;
    maxLoginAttempts: number;
    encryptionEnabled: boolean;
  };
  ui: {
    animationsEnabled: boolean;
    compactMode: boolean;
    autoRefresh: boolean;
    refreshInterval: number;
  };
  vault: {
    maxVaults: number;
    autoBackup: boolean;
    compressionEnabled: boolean;
  };
}

export class SystemConfig {
  private logger: Logger;
  private config: SystemConfiguration;
  private defaultConfig: SystemConfiguration = {
    api: {
      baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:PORT',
      timeout: 30000,
      retries: 3
    },
    features: {
      darkMode: true,
      analytics: true,
      notifications: true,
      autoSave: true
    },
    security: {
      sessionTimeout: 3600000, // 1 hour
      maxLoginAttempts: 5,
      encryptionEnabled: true
    },
    ui: {
      animationsEnabled: true,
      compactMode: false,
      autoRefresh: true,
      refreshInterval: 30000
    },
    vault: {
      maxVaults: 100,
      autoBackup: true,
      compressionEnabled: true
    }
  };

  constructor() {
    this.logger = new Logger('SystemConfig');
    this.config = { ...this.defaultConfig };
  }

  public async load(): Promise<void> {
    try {
      // Load configuration from environment variables
      this.loadFromEnvironment();

      // Load configuration from remote source if available
      await this.loadFromRemote();

      // Validate configuration
      this.validateConfig();

      this.logger.info('✅ System configuration loaded successfully');
    } catch (error) {
      this.logger.error('❌ Failed to load system configuration:', error);
      // Fall back to default configuration
      this.config = { ...this.defaultConfig };
    }
  }

  private loadFromEnvironment(): void {
    // API Configuration
    if (process.env.REACT_APP_API_URL) {
      this.config.api.baseUrl = process.env.REACT_APP_API_URL;
    }
    if (process.env.REACT_APP_API_TIMEOUT) {
      this.config.api.timeout = parseInt(process.env.REACT_APP_API_TIMEOUT, 10);
    }

    // Feature Flags
    if (process.env.REACT_APP_DARK_MODE !== undefined) {
      this.config.features.darkMode = process.env.REACT_APP_DARK_MODE === 'true';
    }
    if (process.env.REACT_APP_ANALYTICS !== undefined) {
      this.config.features.analytics = process.env.REACT_APP_ANALYTICS === 'true';
    }

    // Security Configuration
    if (process.env.REACT_APP_SESSION_TIMEOUT) {
      this.config.security.sessionTimeout = parseInt(process.env.REACT_APP_SESSION_TIMEOUT, 10);
    }

    this.logger.debug('Configuration loaded from environment variables');
  }

  private async loadFromRemote(): Promise<void> {
    try {
      // In a real implementation, this would fetch from a remote config service
      // For now, we'll skip remote configuration loading
      this.logger.debug('Remote configuration loading skipped');
    } catch (error) {
      this.logger.warn('Failed to load remote configuration:', error);
    }
  }

  private validateConfig(): void {
    // Validate API configuration
    if (!this.config.api.baseUrl) {
      throw new Error('API base URL is required');
    }
    if (this.config.api.timeout < 1000) {
      this.logger.warn('API timeout is very low, setting to minimum 1000ms');
      this.config.api.timeout = 1000;
    }

    // Validate security configuration
    if (this.config.security.sessionTimeout < 60000) {
      this.logger.warn('Session timeout is very low, setting to minimum 1 minute');
      this.config.security.sessionTimeout = 60000;
    }

    this.logger.debug('Configuration validation completed');
  }

  public get<K extends keyof SystemConfiguration>(key: K): SystemConfiguration[K] {
    return this.config[key];
  }

  public getAll(): SystemConfiguration {
    return { ...this.config };
  }

  public update<K extends keyof SystemConfiguration>(
    key: K,
    value: Partial<SystemConfiguration[K]>
  ): void {
    this.config[key] = { ...this.config[key], ...value };
    this.logger.debug(`Configuration updated: ${key}`, value);
  }

  public isFeatureEnabled(feature: keyof SystemConfiguration['features']): boolean {
    return this.config.features[feature];
  }

  public getApiConfig() {
    return this.config.api;
  }

  public getSecurityConfig() {
    return this.config.security;
  }
}

export default SystemConfig;
