---
argument-hint: [type] [component] [format]
description: Generate comprehensive technical documentation for Legal Evidence Analysis System
allowed-tools: Read, Write, Bash, Grep, Glob, TodoWrite
agent: documentation-generator
---

# 📚 Project Documentation Generator

**Documentation Request**: $ARGUMENTS

Generate professional, court-ready technical documentation for our Legal Evidence Analysis System using specialized forensic documentation standards.

## Available Documentation Types:

### API Documentation
- `/project-docs api` - Complete API reference with OpenAI Responses patterns
- `/project-docs api core` - Core analyzer API documentation
- `/project-docs api models` - Pydantic legal evidence models
- `/project-docs api cli` - Command-line interface documentation
- Includes cost transparency ($0.0014 per image) and optimization strategies

### Architecture Documentation
- `/project-docs architecture` - V2 system design and component interactions
- `/project-docs architecture flow` - Data flow and evidence processing pipeline
- `/project-docs architecture security` - Security patterns and legal compliance
- `/project-docs architecture scaling` - Performance and parallel processing design

### Legal Compliance Documentation
- `/project-docs legal` - UK employment law compliance guidelines
- `/project-docs legal evidence` - Evidence chain and custody requirements
- `/project-docs legal standards` - Court-ready documentation standards
- `/project-docs legal gdpr` - Data protection and privacy compliance

### User Guides
- `/project-docs user` - Complete user guide for legal professionals
- `/project-docs user cli` - Command-line usage patterns and workflows
- `/project-docs user batch` - Batch processing for large evidence sets
- `/project-docs user troubleshooting` - Common issues and solutions

### Developer Documentation
- `/project-docs dev` - Developer setup and contribution guidelines
- `/project-docs dev models` - Pydantic schema extensions and customization
- `/project-docs dev integration` - Embedding in legal evidence workflows
- `/project-docs dev testing` - Testing strategies for forensic accuracy

### Code Documentation
- `/project-docs code` - Generate comprehensive docstrings and comments
- `/project-docs code models` - Document Pydantic models with legal context
- `/project-docs code functions` - Function documentation with forensic context
- `/project-docs code schemas` - JSON schema documentation for legal evidence

## Output Formats:

### Standard Documentation
- **Markdown**: Professional documentation with legal context
- **API Reference**: Complete interface documentation with examples
- **Compliance Reports**: Legal framework adherence documentation
- **Cost Analysis**: Transparent pricing and optimization guides

### Legal-Ready Formats
- **Expert Witness**: Documentation suitable for tribunal review
- **Technical Reports**: Court-ready technical analysis documentation
- **Compliance Audits**: Regulatory adherence verification reports
- **Evidence Chain**: Custody and traceability documentation

## Documentation Standards Applied:

### Technical Accuracy
- ✅ Correct OpenAI Responses API patterns (never ChatCompletions)
- ✅ Current cost calculations and transparency
- ✅ Thread-safe concurrent processing documentation
- ✅ Proper error handling and edge case coverage

### Legal Compliance
- ✅ Professional language suitable for legal proceedings
- ✅ Objective, bias-free technical content
- ✅ UK employment law framework integration
- ✅ GDPR and data protection considerations

### Code Quality
- ✅ Complete type annotations and interface documentation
- ✅ Working code examples with realistic legal scenarios
- ✅ Comprehensive docstrings with forensic context
- ✅ Architecture diagrams and component relationships

## Automated Features:

### Documentation Sync
- **Hook Integration**: Works with `check_docs_sync.py` for validation
- **Version Control**: Tracks documentation changes with code changes
- **Format Enforcement**: Uses `format_on_write.py` for consistency
- **Standards Compliance**: Integrates with `project_standards_enforcer.py`

### Quality Assurance
- **Technical Validation**: Verifies all code examples execute successfully
- **Legal Review**: Ensures content meets tribunal standards
- **Completeness Check**: Validates all public interfaces are documented
- **Cross-Reference**: Maintains navigation and reference integrity

## Usage Examples:

### Generate Complete API Documentation
```bash
# Complete API reference
/project-docs api

# Focus on specific component
/project-docs api core-analyzer

# Include cost optimization guide
/project-docs api cost-optimization
```

### Create Legal Compliance Documentation
```bash
# Full legal compliance guide
/project-docs legal

# GDPR-specific documentation
/project-docs legal gdpr

# Evidence chain documentation
/project-docs legal evidence-chain
```

### Generate User Documentation
```bash
# Complete user guide
/project-docs user

# CLI-specific guide
/project-docs user cli

# Troubleshooting guide
/project-docs user troubleshooting
```

### Update Code Documentation
```bash
# Generate all docstrings
/project-docs code

# Focus on models
/project-docs code models

# Document specific functions
/project-docs code analyze-functions
```

## Integration Benefits:

### Legal Evidence Workflow
- **Court-Ready**: Documentation meets UK employment tribunal standards
- **Expert Witness**: Technical content suitable for legal expert review
- **Evidence Chain**: Maintains custody and traceability requirements
- **Compliance**: Adheres to GDPR and employment law frameworks

### Development Workflow
- **Automated Updates**: Documentation stays current with code changes
- **Quality Gates**: Ensures all public interfaces are documented
- **Standards Enforcement**: Maintains professional documentation quality
- **Integration**: Works seamlessly with existing development hooks

### Team Collaboration
- **Shared Standards**: Consistent documentation across all components
- **Legal Context**: Technical documentation with forensic awareness
- **Accessibility**: Clear for legal professionals with limited technical background
- **Maintenance**: Automated validation and update processes

The documentation generator creates comprehensive, legally-compliant technical documentation that meets both development needs and court-ready evidence standards for UK employment law proceedings.