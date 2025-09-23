---
argument-hint: [code|docs|tests|setup] [specific-target]
description: Validate different aspects of the project for quality and completeness
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
---

# ✅ Project Validation

**Target**: $ARGUMENTS

Perform comprehensive validation checks on your project to ensure quality, completeness, and readiness.

## Available Validation Types:

### Code Quality
- `/validate code` - Run all code quality checks
- `/validate code auth-module` - Validate specific code module
- Check linting, type checking, formatting
- Analyze code complexity and maintainability
- Review security and best practices

### Documentation
- `/validate docs` - Check documentation completeness
- `/validate docs api` - Validate specific documentation section
- Verify README accuracy and completeness
- Check inline code documentation
- Validate example code and tutorials

### Test Coverage
- `/validate tests` - Run comprehensive test validation
- `/validate tests integration` - Check specific test type
- Measure test coverage and quality
- Identify untested code paths
- Validate test data and fixtures

### Project Setup
- `/validate setup` - Check project configuration
- `/validate setup dependencies` - Validate specific setup aspect
- Verify build processes and scripts
- Check environment configuration
- Validate CI/CD pipeline setup

## Validation Outputs:
- Detailed quality reports
- Actionable improvement recommendations
- TodoWrite tasks for addressing issues
- Compliance and readiness checklists

## Integration Benefits:
- Pre-commit validation workflows
- CI/CD quality gates
- Team onboarding verification
- Release readiness checks

The validation process creates TodoWrite tasks for any issues found, making it easy to track and address quality improvements systematically.