#!/bin/bash

echo "🔥 NUCLEAR VENV REBUILD - Python 3.13.5 Fortress Protocol"
echo "=================================================="

# Set Python version via pyenv
echo "📍 Setting Python 3.13.5 via pyenv..."
pyenv install 3.13.5 --skip-existing
pyenv local 3.13.5

# Nuclear reset of virtual environment
echo "💣 Nuclear VENV reset..."
rm -rf .venv
python3.13 -m venv .venv
source .venv/bin/activate

# Upgrade pip and essential tools
echo "📦 Installing essential packages..."
pip install --upgrade pip setuptools wheel

# Install core dependencies
pip install pre-commit black isort flake8 rich typer

# Install pre-commit hooks
echo "🧠 Installing pre-commit hooks..."
pre-commit install

# Verify Python version
echo "✅ Verification:"
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"

echo "🌌 FORTRESS LOCKDOWN COMPLETE ✅"
echo "🔒 Environment rebuilt and locked to Python 3.13.5"
echo "🛡️ Pre-commit hooks active with version guard"
echo "⚡ Ready for immortal commits!"
echo ""
echo "Usage:"
echo "  source .venv/bin/activate  # Activate environment"
echo "  git add . && git commit    # Commit with full validation"
