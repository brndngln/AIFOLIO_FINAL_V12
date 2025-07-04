#!/bin/bash

echo "⚠️  Starting full AIFOLIO frontend repair sequence..."

cd /Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/frontend || {
  echo "❌ Frontend folder not found. Aborting."
  exit 1
}

echo "🧹 Cleaning environment..."
rm -rf node_modules
rm -f package-lock.json
rm -f .eslintcache

echo "📦 Installing fresh dependencies..."
npm install

echo "🔧 Resetting ESLint config..."
cat <<EOL > .eslintrc.js
module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  parser: '@babel/eslint-parser',
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module',
    requireConfigFile: false,
  },
  extends: ['eslint:recommended', 'plugin:react/recommended'],
  plugins: ['react'],
  rules: {
    'react/prop-types': 'off',
    'no-unused-vars': 'warn',
    'no-console': 'off',
    'react/react-in-jsx-scope': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
EOL

echo "🔌 Installing ESLint plugins..."
npm install --save-dev eslint @babel/eslint-parser eslint-plugin-react

echo "🛠 Running ESLint fix on all source files..."
npx eslint src --ext .js,.jsx,.ts,.tsx --fix

echo "✅ All done. Frontend cleaned, reinstalled, and fixed!"
