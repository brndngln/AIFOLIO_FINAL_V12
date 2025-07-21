#!/bin/bash

# AIFOLIO Elite System - Development Server Launcher
# Cross-platform compatible (Linux/macOS)
# Intelligent package manager detection and dev server startup

set -e  # Exit on any error

echo "🚀 AIFOLIO: Launching development server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if file exists
file_exists() {
    [ -f "$1" ]
}

# Detect package manager and run appropriate dev command
detect_and_run() {
    local package_manager=""
    local dev_command=""

    # Check for package manager preference in order of preference
    if file_exists "pnpm-lock.yaml" && command_exists "pnpm"; then
        package_manager="pnpm"
        dev_command="pnpm dev"
    elif file_exists "yarn.lock" && command_exists "yarn"; then
        package_manager="yarn"
        dev_command="yarn dev"
    elif file_exists "package-lock.json" && command_exists "npm"; then
        package_manager="npm"
        dev_command="npm run dev"
    elif command_exists "npm"; then
        package_manager="npm"
        dev_command="npm run dev"
    else
        echo "❌ No package manager found (npm, yarn, or pnpm)"
        echo "Please install Node.js and npm first"
        exit 1
    fi

    echo "📦 Detected package manager: $package_manager"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "⚠️  node_modules not found. Installing dependencies..."

        case $package_manager in
            "pnpm")
                pnpm install
                ;;
            "yarn")
                yarn install
                ;;
            "npm")
                npm install
                ;;
        esac

        echo "✅ Dependencies installed"
    fi

    # Check if package.json has dev script
    if ! grep -q '"dev"' package.json 2>/dev/null && ! grep -q '"dev"' config/package.json 2>/dev/null; then
        echo "⚠️  No 'dev' script found in package.json"
        echo "Trying alternative development commands..."

        # Try common alternatives
        case $package_manager in
            "pnpm")
                if grep -q '"start"' package.json 2>/dev/null; then
                    dev_command="pnpm start"
                elif grep -q '"serve"' package.json 2>/dev/null; then
                    dev_command="pnpm serve"
                else
                    echo "❌ No suitable development script found"
                    exit 1
                fi
                ;;
            "yarn")
                if grep -q '"start"' package.json 2>/dev/null; then
                    dev_command="yarn start"
                elif grep -q '"serve"' package.json 2>/dev/null; then
                    dev_command="yarn serve"
                else
                    echo "❌ No suitable development script found"
                    exit 1
                fi
                ;;
            "npm")
                if grep -q '"start"' package.json 2>/dev/null; then
                    dev_command="npm start"
                elif grep -q '"serve"' package.json 2>/dev/null; then
                    dev_command="npm run serve"
                else
                    echo "❌ No suitable development script found"
                    exit 1
                fi
                ;;
        esac
    fi

    echo "🎯 Running: $dev_command"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 Development server starting..."
    echo "📱 PWA features enabled"
    echo "🎨 Theme system active"
    echo "🔧 Hot reload enabled"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Execute the development command
    exec $dev_command
}

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -f "config/package.json" ]; then
    echo "❌ package.json not found. Are you in the project root?"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Set environment for development
export NODE_ENV=development

# Run the detection and execution
detect_and_run
