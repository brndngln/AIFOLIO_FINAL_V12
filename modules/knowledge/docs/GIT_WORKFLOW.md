# 🔒 AIFOLIO Elite Git Workflow

**Immutable Git Protocol + AI Commit Hygiene**

This document outlines the complete Git workflow for the AIFOLIO Elite System, including security protocols, commit standards, and automated quality enforcement.

## 🎯 **Overview**

The AIFOLIO Git system implements a **quantum-grade testing foundation** with:
- **Cryptographic integrity** through optional GPG signing
- **AI-verified commits** via Commitizen and Commitlint
- **Automated quality enforcement** through Husky and Lint-Staged
- **Semantic versioning** with conventional commits
- **Zero technical debt** through comprehensive linting

## 🔧 **Setup & Installation**

### Quick Setup
```bash
# Run the automated setup script
./scripts/setup-git-security.sh

# Or install manually:
npm install --save-dev husky lint-staged @commitlint/cli @commitlint/config-conventional commitizen cz-conventional-changelog
```

### Git Aliases Installation
```bash
# Install AIFOLIO Git aliases
git config --global include.path "$(pwd)/config/.gitconfig-aliases"
```

## 🚀 **Daily Workflow**

### 1. **Starting Work**
```bash
# Get latest changes
git reload              # Fetch and rebase from origin

# Create feature branch
git feature my-feature  # Creates feature/my-feature branch
git hotfix urgent-fix   # Creates hotfix/urgent-fix branch
```

### 2. **Making Changes**
```bash
# Check status
git scan               # Quick status overview

# Stage changes
git aa                 # Stage all changes
git ap                 # Interactive staging (patch mode)
```

### 3. **Committing Changes**
```bash
# Semantic commit (RECOMMENDED)
npm run commit         # Interactive Commitizen prompt
git ship              # Stage all + commit with Commitizen

# Manual commit (discouraged)
git commit -m "feat: add new feature"
```

### 4. **Reviewing Changes**
```bash
# View changes
git lg                # Beautiful commit log
git changes           # Show changed files
git staged            # Show staged changes
git wdiff             # Word-level diff highlighting
```

### 5. **Syncing & Deployment**
```bash
# Push changes
git push-current      # Push current branch with upstream tracking

# Deploy
git deploy-staging    # Deploy to staging environment
git deploy-prod       # Deploy to production (with confirmation)
```

## 📝 **Commit Message Standards**

### Conventional Commit Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **ci**: CI/CD changes
- **build**: Build system changes
- **security**: Security fixes
- **ui**: UI/UX changes
- **api**: API changes
- **hotfix**: Critical hotfixes

### Examples
```bash
# Good commits
feat(auth): add OAuth2 integration
fix(ui): resolve button alignment issue
docs(readme): update installation instructions
perf(api): optimize database queries
security(auth): patch JWT vulnerability

# Bad commits (will be rejected)
"fixed stuff"
"WIP"
"temp commit"
"asdf"
```

## 🛡️ **Security Features**

### Pre-Commit Hooks
- **Lint-Staged**: Automatically formats and lints code
- **Prettier**: Code formatting enforcement
- **ESLint**: Code quality validation
- **TypeScript**: Type checking

### Commit Message Validation
- **Commitlint**: Enforces conventional commit format
- **Length limits**: Subject ≤ 72 chars, header ≤ 100 chars
- **Case sensitivity**: lowercase types and scopes
- **Required fields**: type and subject mandatory

### GPG Signing (Optional)
```bash
# Enable GPG signing
git config --global commit.gpgsign true
git config --global user.signingkey YOUR_GPG_KEY_ID

# Verify signatures
git log --show-signature
```

## 🔧 **Git Aliases Reference**

### Status & Information
```bash
git lg                # Beautiful commit log with graph
git scan              # Quick status overview
git br                # Show branches with last commit
git recent            # Show branches by date
```

### Commit & Staging
```bash
git ship              # Stage all + semantic commit
git save              # Quick WIP commit
git amend             # Amend last commit
git redo              # Amend with new message
```

### Undo & Reset
```bash
git undo              # Soft reset last commit
git wipe              # Hard reset (with confirmation)
git unstage           # Unstage files
git discard           # Discard working directory changes
```

### Remote & Sync
```bash
git reload            # Fetch + rebase from origin
git push-current      # Push current branch with tracking
git force             # Force push with lease (safer)
git sync              # Sync with upstream
```

### Branch Management
```bash
git nb branch-name    # Create and switch to new branch
git co branch-name    # Switch to branch
git prune             # Delete merged branches
git recent            # Show branches by date
```

### Search & Maintenance
```bash
git find "search"     # Search commit messages
git contributors      # Show contributors
git optimize          # Optimize repository
git verify            # Verify repository integrity
```

## 🚨 **Emergency Procedures**

### Emergency Commit (Bypass Hooks)
```bash
git emergency "critical fix description"
```

### Recovery Commands
```bash
git history           # Show reflog
git recover branch    # Recover deleted branch
git goto commit-hash  # Reset to specific commit
```

### Repository Maintenance
```bash
git optimize          # Garbage collection + repack
git size              # Show repository size
git verify            # Check repository integrity
```

## 🛑 **Rules of Engagement**

### ❌ **FORBIDDEN ACTIONS**
- ❌ Direct commits without `npm run commit` or `git ship`
- ❌ Committing `.env` files or sensitive data
- ❌ Direct commits to `main` or `develop` branches
- ❌ Bypassing pre-commit hooks (except emergencies)
- ❌ Force pushing without `--force-with-lease`
- ❌ Unstructured commit messages
- ❌ Committing with WIP or temporary messages

### ✅ **REQUIRED PRACTICES**
- ✅ Use semantic commit messages
- ✅ Run tests before committing
- ✅ Format code with Prettier
- ✅ Fix ESLint warnings
- ✅ Use feature branches for development
- ✅ Rebase instead of merge when possible
- ✅ Sign commits with GPG (if enabled)

## 🔍 **Troubleshooting**

### Pre-Commit Hook Failures
```bash
# Fix formatting issues
npx prettier --write .
npx eslint --fix .

# Skip hooks in emergency (use sparingly)
git commit --no-verify -m "emergency: description"
```

### Commit Message Rejected
```bash
# Use Commitizen for proper format
npm run commit

# Or follow conventional commit format manually
git commit -m "type(scope): description"
```

### GPG Signing Issues
```bash
# Set GPG TTY
export GPG_TTY=$(tty)

# Test GPG signing
echo "test" | gpg --clearsign

# Restart GPG agent
gpgconf --kill gpg-agent
```

## 📊 **Quality Metrics**

### Commit Quality Indicators
- **Semantic compliance**: 100% conventional commits
- **Code quality**: All ESLint rules passing
- **Formatting**: Consistent Prettier formatting
- **Test coverage**: Maintained or improved
- **Security**: No sensitive data committed

### Repository Health
- **Branch hygiene**: Regular pruning of merged branches
- **Commit frequency**: Regular, atomic commits
- **Message clarity**: Descriptive, imperative mood
- **History cleanliness**: Linear history with rebasing

## 🎓 **Best Practices**

### Commit Frequency
- **Atomic commits**: One logical change per commit
- **Regular commits**: Commit early and often
- **Meaningful messages**: Explain the "why", not just "what"

### Branch Strategy
- **Feature branches**: `feature/description`
- **Hotfix branches**: `hotfix/description`
- **Release branches**: `release/version`
- **Short-lived branches**: Merge quickly to avoid conflicts

### Code Quality
- **Pre-commit validation**: Let tools catch issues early
- **Consistent formatting**: Prettier handles all formatting
- **Type safety**: TypeScript for type checking
- **Test coverage**: Maintain comprehensive test suite

---

## 🏆 **Elite Status Achieved**

When following this workflow, your repository will have:
- 🔐 **Cryptographic integrity** through optional GPG signing
- 🧠 **AI-verified commits** with semantic structure
- ⚡ **Zero technical debt** through automated quality enforcement
- 📈 **Perfect history** with meaningful, searchable commits
- 🛡️ **Security hardened** against accidental data leaks
- 🚀 **Deployment ready** with standardized processes

**Remember**: Use `npm run commit` for all commits to maintain elite status!
