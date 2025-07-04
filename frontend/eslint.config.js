import js from '@eslint/js';
import react from 'eslint-plugin-react';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
  js.config({
    env: {
      browser: true,
      node: true,
      es2021: true,
    },
    parserOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      ecmaFeatures: { jsx: true },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'off',
    },
  }),
  {
    plugins: {
      react,
      '@typescript-eslint': tsPlugin,
    },
    languageOptions: {
      parser: tsParser,
    },
    settings: {
      react: { version: 'detect' },
    },
    rules: {
      'react/prop-types': 'off',
      'react/react-in-jsx-scope': 'off',
    },
  },
];
