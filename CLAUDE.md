# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### ALWAYS CHECK 'source .venv/bin/activate' 

### ALWAYS USE UV PACKAGE MANAGMENT 'uv add', 'uv pip install', 'uv run...' 

### Installation & Setup
```bash
# Install package in development mode
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Core Commands
```bash
# Analyze directory of images
image-analyzer analyze ./images

# Analyze with parallel processing
image-analyzer analyze ./images --parallel 4

# Analyze single image
image-analyzer single image.jpg

# Estimate costs before analysis
image-analyzer estimate ./images

# Run with custom output directory
image-analyzer analyze ./images -o ./evidence_output
```

### Testing
```bash
# Run tests (basic test structure exists)
python -m pytest tests/

# Test CLI functionality
image-analyzer version
image-analyzer estimate examples/sample_images/
```

## Architecture Overview

This is an AI-powered forensic image analysis tool for UK employment law evidence processing. The codebase follows a clean V2 architecture:

### Core Components

1. **Core Analysis Engine** (`src/image_analyzer/core_analyzer.py`)
   - `LegalEvidenceAnalyzer`: Main analysis class using OpenAI GPT-4 Vision API
   - Uses structured outputs with Pydantic models for guaranteed schema compliance
   - Supports both sequential and parallel batch processing
   - Thread-safe cost tracking across concurrent operations

2. **Legal Evidence Models**
   - `LegalEvidence`: Core structured output for forensic analysis
   - `LegalEvidenceWithPath`: Extended model with source file tracking
   - `SeverityLevel` & `EvidenceType` enums for legal classification

3. **Evidence Organization** (`EvidenceOrganizer`)
   - Automatically categorizes evidence by severity and legal type
   - Creates organized directory structure for legal review
   - Generates comprehensive summary reports

4. **CLI Interface** (`src/image_analyzer/cli.py`)
   - Full command-line interface with subcommands
   - Cost estimation and confirmation prompts
   - JSON output support for integration

### Key Design Patterns

- **Structured Analysis**: Uses OpenAI's structured output feature to guarantee consistent legal evidence format
- **Parallel Processing**: ThreadPoolExecutor for concurrent API calls with configurable batch sizes
- **Legal Framework Focus**: Specialized for UK employment law violations and workplace safety
- **Evidence Chain**: Maintains source file tracking and generates court-ready documentation

### API Integration
- Uses OpenAI GPT-4 Vision API via the `responses.create()` method
- Cost tracking: ~$0.0014 per image
- Structured JSON schema enforcement for reliable legal evidence extraction
- Thread-safe cost accumulation across parallel processing

### Dependencies
- `openai>=1.0.0`: Core AI analysis
- `pydantic>=2.0.0`: Data validation and structured outputs
- `Pillow>=10.0.0`: Image processing
- `click>=8.0.0`: CLI framework
- `python-dotenv>=1.0.0`: Environment configuration

## Configuration System

### Pydantic-Based Configuration
The system uses comprehensive Pydantic models for type-safe configuration management:

```python
from config.config import get_config, Environment

# Load environment-specific configuration
config = get_config(Environment.PRODUCTION)

# All configuration is validated at runtime
print(f"Model: {config.openai.model}")
print(f"Confidence threshold: {config.analysis.confidence_threshold}")
print(f"Audit logging: {config.legal.audit_logging}")
```

### Environment Types
- **development**: Conservative settings, gpt-4.1-mini, enhanced logging
- **testing**: Test-optimized configuration with predictable behavior
- **production**: High-performance settings, gpt-4o, optimized parallel processing
- **legal_production**: Maximum security, mandatory audit logging, chain of custody
- **demo**: Cost-optimized for demonstrations

### Configuration Files
```
config/
├── defaults.yaml           # Base configuration
├── environments.yaml       # Environment-specific overrides
├── legal_domains.yaml      # Legal domain configurations
└── user.yaml              # Optional user customizations
```

### Key Features
- **Type Safety**: Full Pydantic validation with error handling
- **Environment Inheritance**: Hierarchical configuration with overrides
- **Legal Domain Specialization**: Domain-specific confidence thresholds and requirements
- **Audit Logging**: Comprehensive audit trails with SHA-256 checksums
- **Chain of Custody**: Complete evidence tracking for legal compliance
- **Cost Controls**: Configurable spending limits and warnings
- **Expert Review**: Automated flagging based on confidence and severity

## Development Notes

- Environment variables: `OPENAI_API_KEY` required, `IMAGE_ANALYZER_ENV` optional
- Configuration validation: Pydantic models ensure type safety and value constraints
- Image formats supported: .jpg, .jpeg, .png, .bmp, .tiff, .webp, .gif
- Output structure follows legal evidence organization patterns
- Parallel processing optimized for API rate limits (configurable workers)
- All analysis results include forensic-quality expert witness notes
- Audit logging creates JSON audit trails and chain of custody documentation

## Legal Compliance Focus

The system specializes in UK employment law frameworks:
- Health & Safety at Work Act 1974
- Workplace (Health, Safety and Welfare) Regulations 1992
- Management of Health and Safety at Work Regulations 1999
- Control of Substances Hazardous to Health Regulations 2002
- Food Safety and Hygiene Regulations