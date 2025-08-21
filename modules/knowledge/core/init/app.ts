/**
 * AIFOLIO™ Core Application Initializer
 * Elite modular architecture - Entry point for system initialization
 */

import { GlobalState } from '../state/globalState';
import { SystemConfig } from '../system/config';
import { Logger } from '../../lib/utils/logger';

export class AIFOLIOApp {
  private static instance: AIFOLIOApp;
  private globalState: GlobalState;
  private systemConfig: SystemConfig;
  private logger: Logger;

  private constructor() {
    this.logger = new Logger('AIFOLIOApp');
    this.systemConfig = new SystemConfig();
    this.globalState = new GlobalState();
  }

  public static getInstance(): AIFOLIOApp {
    if (!AIFOLIOApp.instance) {
      AIFOLIOApp.instance = new AIFOLIOApp();
    }
    return AIFOLIOApp.instance;
  }

  public async initialize(): Promise<void> {
    try {
      this.logger.info('🚀 Initializing AIFOLIO™ Core System...');

      // Initialize system configuration
      await this.systemConfig.load();

      // Initialize global state
      await this.globalState.initialize();

      // Register system-wide event handlers
      this.registerEventHandlers();

      this.logger.info('✅ AIFOLIO™ Core System initialized successfully');
    } catch (error) {
      this.logger.error('❌ Failed to initialize AIFOLIO™ Core System:', error);
      throw error;
    }
  }

  private registerEventHandlers(): void {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.logger.error('Global error:', event.error);
    });

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.logger.error('Unhandled promise rejection:', event.reason);
    });
  }

  public getGlobalState(): GlobalState {
    return this.globalState;
  }

  public getSystemConfig(): SystemConfig {
    return this.systemConfig;
  }
}

export default AIFOLIOApp;
