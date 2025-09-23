---
argument-hint: [performance|architecture|security|dependencies] [target]
description: Deep analysis of code quality, architecture, performance, or security aspects
allowed-tools: Read, Grep, Glob, Bash, TodoWrite
---

# 🔍 Deep Code Analysis

**Analysis Type**: $ARGUMENTS

Perform comprehensive analysis of your codebase using specialized agents for different quality aspects.

## Available Analysis Types:

### Performance Analysis
- `/analyze performance` - Complete performance audit of the codebase
- `/analyze performance database` - Focus on database query optimization
- `/analyze performance frontend` - Frontend rendering and bundle analysis
- `/analyze performance api` - API endpoint and response time analysis
- Uses the performance-optimizer agent for systematic bottleneck identification

### Architecture Review
- `/analyze architecture` - System design and structure evaluation
- `/analyze architecture patterns` - Design pattern usage and consistency
- `/analyze architecture scalability` - Growth and scaling assessment
- `/analyze architecture dependencies` - Component coupling and cohesion analysis
- Uses the architecture-reviewer agent for design validation

### Security Assessment
- `/analyze security` - Comprehensive security vulnerability scan
- `/analyze security auth` - Authentication and authorization review
- `/analyze security data` - Data protection and privacy analysis
- `/analyze security dependencies` - Third-party dependency security audit
- Uses security-focused analysis for threat identification

### Dependency Analysis
- `/analyze dependencies` - Package and module dependency review
- `/analyze dependencies outdated` - Find outdated packages and security issues
- `/analyze dependencies unused` - Identify and remove unused dependencies
- `/analyze dependencies conflicts` - Resolve version conflicts and compatibility

## Analysis Outputs:
- **Detailed reports** with specific findings and recommendations
- **TodoWrite tasks** for addressing identified issues
- **Priority rankings** (Critical, High, Medium, Low)
- **Implementation timelines** and effort estimates
- **Before/after metrics** for tracking improvements

## Integration Benefits:
- **Code quality gates** for CI/CD pipelines
- **Technical debt tracking** with actionable remediation
- **Performance baseline** establishment and monitoring
- **Security compliance** verification and documentation

The analysis commands create comprehensive TodoWrite task lists for systematic improvement of code quality, performance, architecture, and security.