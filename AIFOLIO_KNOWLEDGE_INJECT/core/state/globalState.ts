/**
 * AIFOLIO™ Global State Management
 * Elite modular architecture - Centralized state management
 */

import { BehaviorSubject, Observable } from 'rxjs';
import { Logger } from '../../lib/utils/logger';

export interface GlobalStateData {
  user: UserState | null;
  theme: ThemeState;
  ui: UIState;
  vault: VaultState;
  system: SystemState;
}

export interface UserState {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'viewer';
  permissions: string[];
  isAuthenticated: boolean;
}

export interface ThemeState {
  mode: 'light' | 'dark';
  primaryColor: string;
  accentColor: string;
  customTheme?: Record<string, any>;
}

export interface UIState {
  sidebarOpen: boolean;
  loading: boolean;
  notifications: Notification[];
  modals: Record<string, boolean>;
}

export interface VaultState {
  activeVault: string | null;
  vaults: any[];
  analytics: Record<string, any>;
}

export interface SystemState {
  version: string;
  environment: 'development' | 'staging' | 'production';
  features: Record<string, boolean>;
  maintenance: boolean;
}

export class GlobalState {
  private logger: Logger;
  private stateSubject: BehaviorSubject<GlobalStateData>;
  private initialState: GlobalStateData = {
    user: null,
    theme: {
      mode: 'dark',
      primaryColor: '#6366f1',
      accentColor: '#f59e0b'
    },
    ui: {
      sidebarOpen: true,
      loading: false,
      notifications: [],
      modals: {}
    },
    vault: {
      activeVault: null,
      vaults: [],
      analytics: {}
    },
    system: {
      version: '12.0.0',
      environment: 'development',
      features: {},
      maintenance: false
    }
  };

  constructor() {
    this.logger = new Logger('GlobalState');
    this.stateSubject = new BehaviorSubject<GlobalStateData>(this.initialState);
  }

  public async initialize(): Promise<void> {
    try {
      // Load persisted state from localStorage
      const persistedState = this.loadPersistedState();
      if (persistedState) {
        this.stateSubject.next({ ...this.initialState, ...persistedState });
      }

      // Subscribe to state changes for persistence
      this.stateSubject.subscribe(state => {
        this.persistState(state);
      });

      this.logger.info('✅ Global state initialized');
    } catch (error) {
      this.logger.error('❌ Failed to initialize global state:', error);
      throw error;
    }
  }

  public getState(): Observable<GlobalStateData> {
    return this.stateSubject.asObservable();
  }

  public getCurrentState(): GlobalStateData {
    return this.stateSubject.value;
  }

  public updateState(partialState: Partial<GlobalStateData>): void {
    const currentState = this.stateSubject.value;
    const newState = { ...currentState, ...partialState };
    this.stateSubject.next(newState);
    this.logger.debug('State updated:', partialState);
  }

  public updateUserState(userState: Partial<UserState>): void {
    const currentState = this.stateSubject.value;
    const newUserState = { ...currentState.user, ...userState };
    this.updateState({ user: newUserState });
  }

  public updateTheme(themeState: Partial<ThemeState>): void {
    const currentState = this.stateSubject.value;
    const newThemeState = { ...currentState.theme, ...themeState };
    this.updateState({ theme: newThemeState });
  }

  public updateUI(uiState: Partial<UIState>): void {
    const currentState = this.stateSubject.value;
    const newUIState = { ...currentState.ui, ...uiState };
    this.updateState({ ui: newUIState });
  }

  private loadPersistedState(): Partial<GlobalStateData> | null {
    try {
      const persistedData = localStorage.getItem('aifolio_global_state');
      return persistedData ? JSON.parse(persistedData) : null;
    } catch (error) {
      this.logger.warn('Failed to load persisted state:', error);
      return null;
    }
  }

  private persistState(state: GlobalStateData): void {
    try {
      // Only persist certain parts of the state
      const stateToPersist = {
        theme: state.theme,
        ui: { sidebarOpen: state.ui.sidebarOpen }
      };
      localStorage.setItem('aifolio_global_state', JSON.stringify(stateToPersist));
    } catch (error) {
      this.logger.warn('Failed to persist state:', error);
    }
  }
}

export default GlobalState;
