// AIFOLIO Elite System - Jest Setup
// Global test environment configuration and extensions

import '@testing-library/jest-dom';
import { toHaveNoViolations } from 'jest-axe';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Mock window.matchMedia for responsive design tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver for components that use it
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock ResizeObserver for responsive components
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock sessionStorage
const sessionStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.sessionStorage = sessionStorageMock;

// Mock console methods for cleaner test output
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render is deprecated')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});

// Global test utilities
global.testUtils = {
  // Wait for async operations
  waitFor: (ms = 0) => new Promise(resolve => setTimeout(resolve, ms)),

  // Create mock props
  createMockProps: (overrides = {}) => ({
    'data-testid': 'test-component',
    ...overrides
  }),

  // Mock event handlers
  createMockHandlers: () => ({
    onClick: jest.fn(),
    onChange: jest.fn(),
    onSubmit: jest.fn(),
    onFocus: jest.fn(),
    onBlur: jest.fn(),
  })
};

// Console logging for test debugging
if (process.env.NODE_ENV === 'test' && process.env.DEBUG_TESTS) {
  console.log('🧪 AIFOLIO Test Environment Initialized');
  console.log('⚡ Jest setup complete with enhanced matchers');
  console.log('🎯 Ready for quantum-grade testing');
}
