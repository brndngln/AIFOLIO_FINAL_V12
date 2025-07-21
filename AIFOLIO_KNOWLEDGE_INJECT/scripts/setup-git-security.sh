#!/bin/bash

# AIFOLIO Elite System - Git Security Setup Script
# Configures GitSec™ cryptographic signature enforcement

set -e

echo "🔐 AIFOLIO GitSec™ Setup"
echo "========================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Checking Git configuration..."

# Get current Git user info
GIT_USER_NAME=$(git config --global user.name 2>/dev/null || echo "")
GIT_USER_EMAIL=$(git config --global user.email 2>/dev/null || echo "")

if [ -z "$GIT_USER_NAME" ] || [ -z "$GIT_USER_EMAIL" ]; then
    print_warning "Git user information not configured."
    echo
    read -p "Enter your full name: " USER_NAME
    read -p "Enter your email address: " USER_EMAIL

    git config --global user.name "$USER_NAME"
    git config --global user.email "$USER_EMAIL"

    print_success "Git user information configured."
fi

print_status "Current Git user: $GIT_USER_NAME <$GIT_USER_EMAIL>"

# Configure Git aliases
print_status "Installing AIFOLIO Git aliases..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALIASES_FILE="$SCRIPT_DIR/../config/.gitconfig-aliases"

if [ -f "$ALIASES_FILE" ]; then
    git config --global include.path "$ALIASES_FILE"
    print_success "Git aliases installed successfully."
else
    print_warning "Aliases file not found at $ALIASES_FILE"
fi

# Configure Git settings for security and performance
print_status "Configuring Git security settings..."

# Security settings
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.default simple
git config --global core.autocrlf false
git config --global core.eol lf
git config --global core.fileMode false

# Performance settings
git config --global core.preloadindex true
git config --global core.fscache true
git config --global gc.auto 256

print_success "Git security settings configured."

# GPG signing setup (optional)
echo
print_status "Setting up GPG commit signing (optional)..."
echo "This will enable cryptographic signatures for all commits."
echo

read -p "Do you want to enable GPG commit signing? (y/N): " ENABLE_GPG

if [[ $ENABLE_GPG =~ ^[Yy]$ ]]; then
    # Check if GPG is installed
    if ! command -v gpg &> /dev/null; then
        print_error "GPG is not installed. Please install GPG first:"
        echo "  macOS: brew install gnupg"
        echo "  Ubuntu: sudo apt install gnupg"
        echo "  Windows: Download from https://gnupg.org/download/"
        exit 1
    fi

    # List existing GPG keys
    print_status "Checking for existing GPG keys..."
    GPG_KEYS=$(gpg --list-secret-keys --keyid-format LONG 2>/dev/null | grep sec || echo "")

    if [ -z "$GPG_KEYS" ]; then
        print_warning "No GPG keys found. Creating a new GPG key..."
        echo
        echo "Please follow the prompts to create a new GPG key:"
        echo "1. Choose RSA and RSA (default)"
        echo "2. Choose 4096 bits"
        echo "3. Choose key expiration (recommend 1y)"
        echo "4. Enter your name and email (must match Git config)"
        echo

        gpg --full-generate-key

        print_success "GPG key created successfully."
    fi

    # Get the GPG key ID
    print_status "Available GPG keys:"
    gpg --list-secret-keys --keyid-format LONG
    echo

    read -p "Enter the GPG key ID to use for signing (long format): " GPG_KEY_ID

    if [ -n "$GPG_KEY_ID" ]; then
        # Configure Git to use the GPG key
        git config --global user.signingkey "$GPG_KEY_ID"
        git config --global commit.gpgsign true
        git config --global tag.gpgsign true

        # Configure GPG TTY for terminal use
        echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
        echo 'export GPG_TTY=$(tty)' >> ~/.zshrc

        print_success "GPG signing enabled for all commits and tags."
        print_status "GPG Key ID: $GPG_KEY_ID"

        # Show public key for GitHub/GitLab
        echo
        print_status "Your public GPG key (add this to GitHub/GitLab):"
        echo "=================================================="
        gpg --armor --export "$GPG_KEY_ID"
        echo "=================================================="
        echo
        print_warning "Copy the above public key and add it to your Git hosting service:"
        echo "  GitHub: Settings > SSH and GPG keys > New GPG key"
        echo "  GitLab: Preferences > GPG Keys"

    else
        print_warning "No GPG key ID provided. Skipping GPG setup."
    fi
else
    print_status "GPG signing disabled. You can enable it later by running this script again."
fi

# Configure commit template (optional)
echo
read -p "Do you want to set up a commit message template? (y/N): " SETUP_TEMPLATE

if [[ $SETUP_TEMPLATE =~ ^[Yy]$ ]]; then
    TEMPLATE_FILE="$HOME/.gitmessage"

    cat > "$TEMPLATE_FILE" << 'EOF'
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Type should be one of the following:
# * feat: A new feature
# * fix: A bug fix
# * docs: Documentation changes
# * style: Code style changes (formatting, etc.)
# * refactor: Code refactoring
# * perf: Performance improvements
# * test: Adding or updating tests
# * chore: Maintenance tasks
# * ci: CI/CD changes
# * build: Build system changes
# * revert: Revert previous commit
# * security: Security fixes
# * deps: Dependency updates
# * config: Configuration changes
# * ui: UI/UX changes
# * data: Data changes
# * api: API changes
# * db: Database changes
# * deploy: Deployment changes
# * hotfix: Critical hotfixes

# Remember:
# - Use imperative mood in subject line
# - Do not end subject line with period
# - Separate subject from body with blank line
# - Use body to explain what and why vs. how
# - Can use multiple lines with "-" for bullet points in body
EOF

    git config --global commit.template "$TEMPLATE_FILE"
    print_success "Commit message template configured at $TEMPLATE_FILE"
fi

# Final status
echo
echo "🎉 GitSec™ Setup Complete!"
echo "=========================="
print_success "Git security configuration completed successfully."
echo
print_status "Available commands:"
echo "  npm run commit     - Use Commitizen for structured commits"
echo "  git ship          - Stage all and commit with Commitizen"
echo "  git lg            - Beautiful commit log"
echo "  git scan          - Quick status check"
echo "  git wipe          - Reset working directory (with confirmation)"
echo "  git reload        - Fetch and rebase from origin"
echo "  git prune         - Clean up merged branches"
echo
print_status "Security features enabled:"
echo "  ✅ Husky pre-commit hooks"
echo "  ✅ Lint-staged code formatting"
echo "  ✅ Commitlint message validation"
echo "  ✅ Conventional commit enforcement"
if [[ $ENABLE_GPG =~ ^[Yy]$ ]] && [ -n "$GPG_KEY_ID" ]; then
    echo "  ✅ GPG commit signing"
else
    echo "  ⚠️  GPG commit signing (disabled)"
fi
echo
print_warning "Remember to use 'npm run commit' instead of 'git commit' for semantic commits!"
echo
