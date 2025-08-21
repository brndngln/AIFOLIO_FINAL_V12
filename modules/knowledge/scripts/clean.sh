#!/bin/bash

# AIFOLIO Elite System - Environment Cleanup Script
# Cross-platform compatible (Linux/macOS)
# Removes build artifacts, caches, and temporary files

set -e  # Exit on any error

echo "🧹 AIFOLIO: Cleaning project environment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to safely remove directories/files
safe_remove() {
    local path="$1"
    local description="$2"

    if [ -e "$path" ]; then
        echo "🗑️  Removing $description..."
        rm -rf "$path"
        echo "✅ $description removed"
    else
        echo "ℹ️  $description not found (already clean)"
    fi
}

# Build artifacts
safe_remove "dist" "Distribution folder"
safe_remove "build" "Build folder"
safe_remove ".next" "Next.js build cache"
safe_remove "out" "Static export folder"

# Cache directories
safe_remove ".cache" "General cache"
safe_remove ".turbo" "Turbo cache"
safe_remove ".vite" "Vite cache"
safe_remove ".parcel-cache" "Parcel cache"
safe_remove ".nuxt" "Nuxt cache"

# Node.js
safe_remove "node_modules" "Node modules"
safe_remove "npm-debug.log*" "NPM debug logs"
safe_remove "yarn-debug.log*" "Yarn debug logs"
safe_remove "yarn-error.log*" "Yarn error logs"
safe_remove "lerna-debug.log*" "Lerna debug logs"

# Package manager lock files (optional - uncomment if needed)
# safe_remove "package-lock.json" "NPM lock file"
# safe_remove "yarn.lock" "Yarn lock file"
# safe_remove "pnpm-lock.yaml" "PNPM lock file"

# Test coverage
safe_remove "coverage" "Test coverage reports"
safe_remove ".nyc_output" "NYC coverage output"

# IDE and editor files
safe_remove ".vscode/settings.json" "VSCode workspace settings"
safe_remove ".idea" "IntelliJ IDEA files"

# OS generated files
safe_remove ".DS_Store" "macOS DS_Store files"
safe_remove "Thumbs.db" "Windows thumbnail cache"
safe_remove "*.tmp" "Temporary files"
safe_remove "*.temp" "Temporary files"

# Log files
safe_remove "*.log" "Log files"
safe_remove "logs" "Log directory"

# Temporary directories
safe_remove "tmp" "Temporary directory"
safe_remove "temp" "Temporary directory"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ AIFOLIO: Environment cleaned successfully!"
echo "🚀 Ready for fresh installation and development"
echo ""
echo "Next steps:"
echo "  1. Run: npm install (or yarn install)"
echo "  2. Run: ./scripts/dev.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
