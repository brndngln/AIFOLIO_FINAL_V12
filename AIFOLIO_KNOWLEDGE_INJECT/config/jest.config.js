// AIFOLIO Elite System - Jest Configuration
// Quantum-grade testing foundation with comprehensive setup

module.exports = {
  // Test environment
  testEnvironment: "jsdom",

  // Setup files
  setupFilesAfterEnv: [
    "<rootDir>/config/jest.setup.js"
  ],

  // Transform configuration
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
  },

  // Module name mapping for path aliases
  moduleNameMapping: {
    "^@/(.*)$": "<rootDir>/$1",
    "^@ui/(.*)$": "<rootDir>/ui/$1",
    "^@hooks/(.*)$": "<rootDir>/hooks/$1",
    "^@layouts/(.*)$": "<rootDir>/layouts/$1",
    "^@features/(.*)$": "<rootDir>/features/$1",
    "^@core/(.*)$": "<rootDir>/core/$1"
  },

  // Test file patterns
  testMatch: [
    "<rootDir>/__tests__/**/*.(test|spec).[jt]s?(x)",
    "<rootDir>/**/*.(test|spec).[jt]s?(x)"
  ],

  // Coverage configuration
  collectCoverageFrom: [
    "ui/**/*.{js,jsx,ts,tsx}",
    "hooks/**/*.{js,jsx,ts,tsx}",
    "layouts/**/*.{js,jsx,ts,tsx}",
    "features/**/*.{js,jsx,ts,tsx}",
    "core/**/*.{js,jsx,ts,tsx}",
    "!**/*.d.ts",
    "!**/node_modules/**",
    "!**/dist/**",
    "!**/build/**"
  ],

  // Coverage thresholds (bootstrap level)
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50
    }
  },

  // Module file extensions
  moduleFileExtensions: [
    "js",
    "jsx",
    "ts",
    "tsx",
    "json"
  ],

  // Test timeout
  testTimeout: 10000,

  // Verbose output
  verbose: true,

  // Clear mocks between tests
  clearMocks: true,

  // Restore mocks after each test
  restoreMocks: true
};
