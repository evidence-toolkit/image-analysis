---
argument-hint: [prepare|check|notes|deploy] [version]
description: Comprehensive release management for version preparation, validation, and deployment
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, TodoWrite
---

# 🚀 Release Management

**Release Action**: $ARGUMENTS

Comprehensive release management workflow ensuring quality, consistency, and successful deployments.

## Available Release Operations:

### Prepare Release
- `/release prepare 1.2.0` - Prepare new version release
- `/release prepare patch` - Prepare patch version (1.1.1 → 1.1.2)
- `/release prepare minor` - Prepare minor version (1.1.0 → 1.2.0)
- `/release prepare major` - Prepare major version (1.0.0 → 2.0.0)
- Automated version bumping, changelog generation, and preparation tasks

### Release Validation
- `/release check` - Comprehensive pre-release validation
- `/release check tests` - Run complete test suite with coverage
- `/release check build` - Verify build processes and artifacts
- `/release check security` - Security scan and dependency audit
- Creates TodoWrite tasks for any issues found

### Release Notes
- `/release notes` - Generate release notes from commits and PRs
- `/release notes --since v1.1.0` - Generate notes since specific version
- `/release notes --format markdown` - Specific format output
- Automatic categorization: Features, Bug Fixes, Breaking Changes

### Deployment
- `/release deploy staging` - Deploy to staging environment
- `/release deploy production` - Production deployment
- `/release deploy rollback` - Rollback to previous version
- Automated deployment with validation and monitoring

## Release Workflow:

### 1. Pre-Release Preparation
- **Version planning**: Semantic version determination
- **Code freeze**: Feature completion verification
- **Documentation**: README, API docs, changelog updates
- **Dependencies**: Security updates and compatibility checks

### 2. Quality Assurance
- **Test execution**: Unit, integration, e2e test suites
- **Performance testing**: Load testing and benchmarks
- **Security scanning**: Vulnerability assessment
- **Compatibility testing**: Browser, platform, version support

### 3. Release Artifacts
- **Build generation**: Production-ready artifacts
- **Asset optimization**: Minification, compression, bundling
- **Documentation packaging**: User guides and API references
- **Distribution preparation**: Package registry, CDN uploads

### 4. Deployment Process
- **Staging deployment**: Pre-production validation
- **Production deployment**: Phased rollout with monitoring
- **Health checks**: Post-deployment validation
- **Rollback readiness**: Quick recovery procedures

## Automated Validations:
- ✅ **All tests passing** with adequate coverage
- ✅ **Build artifacts** generated successfully
- ✅ **Security vulnerabilities** resolved
- ✅ **Breaking changes** documented
- ✅ **Performance regressions** checked
- ✅ **Documentation** updated and accurate

## Integration Features:
- **Git tagging** with semantic versions
- **Changelog automation** from commit history
- **CI/CD pipeline** integration and triggering
- **Notification systems** for team communication
- **Rollback procedures** for quick recovery

The release management system creates comprehensive TodoWrite task lists for systematic release preparation, validation, and deployment processes.