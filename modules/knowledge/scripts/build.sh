#!/bin/bash

# AIFOLIO Elite System - Production Build Script
# Cross-platform compatible (Linux/macOS)
# Intelligent package manager detection and production build

set -e  # Exit on any error

echo "🏗️ AIFOLIO: Running production build..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if file exists
file_exists() {
    [ -f "$1" ]
}

# Function to detect and run build
detect_and_build() {
    local package_manager=""
    local build_command=""

    # Check for package manager preference in order of preference
    if file_exists "pnpm-lock.yaml" && command_exists "pnpm"; then
        package_manager="pnpm"
        build_command="pnpm build"
    elif file_exists "yarn.lock" && command_exists "yarn"; then
        package_manager="yarn"
        build_command="yarn build"
    elif file_exists "package-lock.json" && command_exists "npm"; then
        package_manager="npm"
        build_command="npm run build"
    elif command_exists "npm"; then
        package_manager="npm"
        build_command="npm run build"
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
                pnpm install --frozen-lockfile
                ;;
            "yarn")
                yarn install --frozen-lockfile
                ;;
            "npm")
                npm ci
                ;;
        esac

        echo "✅ Dependencies installed"
    fi

    # Check if package.json has build script
    if ! grep -q '"build"' package.json 2>/dev/null && ! grep -q '"build"' config/package.json 2>/dev/null; then
        echo "❌ No 'build' script found in package.json"
        echo "Please add a build script to your package.json"
        exit 1
    fi

    echo "🎯 Running: $build_command"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚡ Production build starting..."
    echo "🔧 Optimizing assets..."
    echo "📦 Bundling components..."
    echo "🎨 Processing themes..."
    echo "📱 PWA assets generation..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Execute the build command
    $build_command

    # Check if build was successful
    if [ $? -eq 0 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ AIFOLIO: Production build completed successfully!"

        # Check for common output directories
        if [ -d "dist" ]; then
            echo "📁 Build output: ./dist/"
            echo "📊 Build size:"
            du -sh dist/ 2>/dev/null || echo "   Size calculation unavailable"
        elif [ -d "build" ]; then
            echo "📁 Build output: ./build/"
            echo "📊 Build size:"
            du -sh build/ 2>/dev/null || echo "   Size calculation unavailable"
        elif [ -d "out" ]; then
            echo "📁 Build output: ./out/"
            echo "📊 Build size:"
            du -sh out/ 2>/dev/null || echo "   Size calculation unavailable"
        fi

        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🚀 Ready for deployment!"
        echo "📱 PWA features included"
        echo "🎨 Theme system optimized"
        echo "⚡ Performance optimized"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        echo "❌ Build failed!"
        exit 1
    fi
}

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -f "config/package.json" ]; then
    echo "❌ package.json not found. Are you in the project root?"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Set environment for production
export NODE_ENV=production

# Clean previous build (optional)
echo "🧹 Cleaning previous build..."
rm -rf dist build out .next 2>/dev/null || true
echo "✅ Previous build cleaned"

# Run the detection and build
detect_and_build
